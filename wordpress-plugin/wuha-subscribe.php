<?php
/**
 * Plugin Name: WUHA Subscribe
 * Description: Newsletter sign-up endpoint for the static wuha.world site. Adds the email to the MailPoet list "English" or "Deutsch" and sends MailPoet's confirmation email (double opt-in).
 * Version: 1.0.0
 * Author: WUHA
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) {
    exit;
}

const WUHA_SUB_ORIGINS = ['https://www.wuha.world', 'https://wuha.world'];
const WUHA_SUB_LIMIT = 5;          // sign-ups per IP …
const WUHA_SUB_WINDOW = HOUR_IN_SECONDS; // … per hour

// admin-ajax.php is used instead of the REST API, which "Disable REST API" blocks for visitors
add_action('wp_ajax_nopriv_wuha_subscribe', 'wuha_sub_ajax');
add_action('wp_ajax_wuha_subscribe', 'wuha_sub_ajax');

function wuha_sub_ajax()
{
    $origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
    if (in_array($origin, WUHA_SUB_ORIGINS, true)) {
        header('Access-Control-Allow-Origin: ' . $origin);
        header('Vary: Origin');
    }
    $res = wuha_sub_handle([
        'origin' => $origin,
        'website' => isset($_POST['website']) ? wp_unslash($_POST['website']) : '',
        'email' => isset($_POST['email']) ? wp_unslash($_POST['email']) : '',
        'lang' => isset($_POST['lang']) ? wp_unslash($_POST['lang']) : 'en',
    ]);
    wp_send_json($res[0], $res[1]);
}

function wuha_sub_error($code, $status)
{
    return [['ok' => false, 'error' => $code], $status];
}

function wuha_sub_find_list($lang)
{
    $const = $lang === 'de' ? 'WUHA_LIST_DE' : 'WUHA_LIST_EN';
    if (defined($const)) {
        return (string) constant($const);
    }
    $pattern = $lang === 'de' ? '/deutsch|german/i' : '/english|englisch/i';
    foreach (\MailPoet\API\API::MP('v1')->getLists() as $list) {
        if (preg_match($pattern, $list['name'])) {
            return (string) $list['id'];
        }
    }
    return null;
}

function wuha_sub_handle(array $in)
{
    $origin = $in['origin'];
    if ($origin && !in_array($origin, WUHA_SUB_ORIGINS, true)) {
        return wuha_sub_error('origin', 403);
    }
    // Honeypot: real visitors never fill this field
    if (trim((string) $in['website']) !== '') {
        return [['ok' => true], 200];
    }
    $ip_key = 'wuha_sub_' . md5((string) ($_SERVER['REMOTE_ADDR'] ?? ''));
    $count = (int) get_transient($ip_key);
    if ($count >= WUHA_SUB_LIMIT) {
        return wuha_sub_error('rate_limit', 429);
    }
    set_transient($ip_key, $count + 1, WUHA_SUB_WINDOW);

    $email = sanitize_email((string) $in['email']);
    if (!is_email($email)) {
        return wuha_sub_error('email', 400);
    }
    $lang = $in['lang'] === 'de' ? 'de' : 'en';

    if (!class_exists('\MailPoet\API\API')) {
        return wuha_sub_error('mailpoet_missing', 500);
    }
    try {
        $list = wuha_sub_find_list($lang);
        if (!$list) {
            return wuha_sub_error('list_missing', 500);
        }
        $mp = \MailPoet\API\API::MP('v1');
        $existing = null;
        try {
            $existing = $mp->getSubscriber($email);
        } catch (\Exception $e) {
            $existing = null;
        }
        if ($existing) {
            $mp->subscribeToLists($existing['id'], [$list], ['send_confirmation_email' => true]);
        } else {
            $mp->addSubscriber(['email' => $email], [$list], ['send_confirmation_email' => true]);
        }
    } catch (\Exception $e) {
        error_log('wuha-subscribe: ' . $e->getMessage());
        return wuha_sub_error('subscribe_failed', 500);
    }
    return [['ok' => true], 200];
}
