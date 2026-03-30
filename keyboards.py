# ═══════════════════════════════════════════════════════════
# KEYBOARDS - FIXED & COMPLETE
# ═══════════════════════════════════════════════════════════

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(is_vip_user=False):
    vip_badge = "⭐ " if is_vip_user else ""
    keyboard = [
        [
            InlineKeyboardButton(f"{vip_badge}🎰 SPIN & WIN", callback_data="spin"),
            InlineKeyboardButton("💰 EARN MONEY", callback_data="earn_menu"),
        ],
        [
            InlineKeyboardButton("🏆 LEADERBOARD", callback_data="leaderboard"),
            InlineKeyboardButton("📊 MY STATS", callback_data="my_stats"),
        ],
        [
            InlineKeyboardButton("👥 REFER FRIENDS", callback_data="refer"),
            InlineKeyboardButton("🏧 WITHDRAW", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton("🎮 PLAY GAMES", callback_data="games"),
            InlineKeyboardButton("🛠️ TOOLS", callback_data="tools"),
        ],
        [
            InlineKeyboardButton("📺 WATCH ADS", callback_data="ads"),
            InlineKeyboardButton("💎 DAILY BONUS", callback_data="daily_bonus"),
        ],
    ]
    if not is_vip_user:
        keyboard.append([
            InlineKeyboardButton("⚡ UPGRADE TO VIP (2x Earnings)", callback_data="vip_upgrade")
        ])
    return InlineKeyboardMarkup(keyboard)


def earn_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎰 Lucky Spin", callback_data="spin"),
            InlineKeyboardButton("👥 Refer Friends", callback_data="refer"),
        ],
        [
            InlineKeyboardButton("📺 Watch Ads", callback_data="ads"),
            InlineKeyboardButton("🎮 Play Games", callback_data="games"),
        ],
        [
            InlineKeyboardButton("⚡ VIP Bonus", callback_data="vip_upgrade"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ],
    ])


def tools_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 URL Shortener (+2)", callback_data="tool_url"),
            InlineKeyboardButton("📸 QR Code (+2)", callback_data="tool_qr"),
        ],
        [
            InlineKeyboardButton("⬇️ YT Downloader (+5)", callback_data="tool_dl"),
            InlineKeyboardButton("🔢 Calculator (+1)", callback_data="tool_calc"),
        ],
        [
            InlineKeyboardButton("🔄 Unit Converter (+1)", callback_data="tool_unit"),
            InlineKeyboardButton("☁️ Weather (+1)", callback_data="tool_weather"),
        ],
        [
            InlineKeyboardButton("🔐 Password Gen (+1)", callback_data="tool_pass"),
            InlineKeyboardButton("📝 Notes (+1)", callback_data="tool_notes"),
        ],
        [
            InlineKeyboardButton("🌐 Site Analyzer (+3)", callback_data="tool_traffic"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ],
    ])


def games_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎯 Guess Number (Win 20)", callback_data="game_guess"),
            InlineKeyboardButton("🎲 Lucky Dice (Win 10)", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🪙 Coin Flip (Win 15)", callback_data="game_coin"),
            InlineKeyboardButton("🎰 Mega Spin (Win 100)", callback_data="game_mega"),
        ],
        [
            InlineKeyboardButton("🏆 Game Leaderboard", callback_data="game_leaderboard"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ],
    ])


def withdraw_menu(available_points, is_vip_user=False):
    tiers = [
        (500, "$5.00"),
        (1000, "$10.00"),
        (2500, "$25.00"),
        (5000, "$50.00"),
        (10000, "$100.00"),
    ]
    buttons = []
    for points, money in tiers:
        if available_points >= points:
            buttons.append([
                InlineKeyboardButton(f"💵 {points} pts = {money}", callback_data=f"wd_{points}")
            ])
    if is_vip_user:
        buttons.append([
            InlineKeyboardButton("⚡ VIP Fast Withdraw (12h)", callback_data="wd_vip_fast")
        ])
    buttons.append([
        InlineKeyboardButton("📋 History", callback_data="wd_history"),
        InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
    ])
    return InlineKeyboardMarkup(buttons)


def payment_methods(amount_points):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 UPI (Free, 24h)",         callback_data=f"pay_upi_{amount_points}")],
        [InlineKeyboardButton("💳 PayPal (5% fee)",         callback_data=f"pay_paypal_{amount_points}")],
        [InlineKeyboardButton("₿ USDT (2% fee, 12h)",       callback_data=f"pay_usdt_{amount_points}")],
        [InlineKeyboardButton("₿ Bitcoin (5% fee)",         callback_data=f"pay_btc_{amount_points}")],
        [InlineKeyboardButton("🏦 Bank Transfer (10% fee)", callback_data=f"pay_bank_{amount_points}")],
        [InlineKeyboardButton("🔙 Back",                    callback_data="withdraw")],
    ])


def vip_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 VIP 1 Month  - $2.99",   callback_data="buy_vip_1")],
        [InlineKeyboardButton("💎💎 VIP 3 Months - $7.99", callback_data="buy_vip_3")],
        [InlineKeyboardButton("💎💎💎 VIP 1 Year - $24.99", callback_data="buy_vip_12")],
        [
            InlineKeyboardButton("📋 Benefits", callback_data="vip_info"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ],
    ])


def referral_share(link):
    share_text = f"🚀 Earn money with FlowX Bot! Free daily spins, real cashout! {link}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📤 Share to Telegram", url=f"https://t.me/share/url?url={link}&text={share_text}")],
        [
            InlineKeyboardButton("📱 WhatsApp", url=f"https://wa.me/?text={share_text}"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu"),
        ],
        [
            InlineKeyboardButton("📊 My Referrals", callback_data="ref_stats"),
        ],
    ])


def ads_menu(ads_list):
    buttons = []
    for ad in ads_list:
        buttons.append([
            InlineKeyboardButton(f"▶️ {ad['title']} (+{ad['points']} pts)", url=ad['url'])
        ])
    buttons.append([
        InlineKeyboardButton("✅ I Watched (Claim)", callback_data="ad_verify"),
        InlineKeyboardButton("🔙 Back", callback_data="earn_menu"),
    ])
    return InlineKeyboardMarkup(buttons)


def leaderboard_tabs():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 Rich List", callback_data="lb_rich"),
            InlineKeyboardButton("👥 Referrals", callback_data="lb_refs"),
        ],
        [
            InlineKeyboardButton("🎰 Spins", callback_data="lb_spins"),
            InlineKeyboardButton("🎮 Games", callback_data="lb_games"),
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ])


def admin_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Stats",    callback_data="admin_stats"),
            InlineKeyboardButton("💰 Pend. WD", callback_data="admin_wd"),
        ],
        [
            InlineKeyboardButton("👥 Users",    callback_data="admin_users"),
            InlineKeyboardButton("📣 Broadcast",callback_data="admin_broadcast"),
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings"),
            InlineKeyboardButton("📋 Logs",     callback_data="admin_logs"),
        ],
    ])


def confirm_cancel(action):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ Cancel",  callback_data="cancel"),
        ]
    ])


def back_button(to="main_menu"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=to)]])
