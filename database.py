# ═══════════════════════════════════════════════════════════
# DATABASE MANAGER - FIXED & COMPLETE
# ═══════════════════════════════════════════════════════════

import sqlite3
import datetime
import threading
from contextlib import contextmanager

DB_FILE = 'flowx_ultimate.db'
db_lock = threading.Lock()

@contextmanager
def get_db():
    """Thread-safe database connection"""
    with db_lock:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

def init_database():
    """Initialize all tables"""
    with get_db() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                referral_code TEXT UNIQUE NOT NULL,
                referred_by INTEGER,
                points INTEGER DEFAULT 0,
                total_earned INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                vip_until TEXT,
                vip_streak INTEGER DEFAULT 0,
                last_spin TEXT,
                last_bonus TEXT,
                streak INTEGER DEFAULT 0,
                login_streak INTEGER DEFAULT 0,
                total_spins INTEGER DEFAULT 0,
                total_refs INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                total_tools INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                banned INTEGER DEFAULT 0,
                warned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referred_by) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount INTEGER NOT NULL,
                balance_after INTEGER,
                description TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS withdrawals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points INTEGER NOT NULL,
                usd_amount REAL NOT NULL,
                fee REAL DEFAULT 0,
                net_amount REAL NOT NULL,
                method TEXT NOT NULL,
                payment_details TEXT,
                transaction_id TEXT,
                status TEXT DEFAULT 'pending',
                status_reason TEXT,
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TEXT,
                completed_at TEXT,
                processed_by INTEGER,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS spin_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points_won INTEGER NOT NULL,
                multiplier REAL DEFAULT 1.0,
                is_jackpot INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS referral_earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER NOT NULL,
                referred_id INTEGER NOT NULL,
                level INTEGER DEFAULT 1,
                points_earned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(telegram_id),
                FOREIGN KEY (referred_id) REFERENCES users(telegram_id),
                UNIQUE(referrer_id, referred_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                game_type TEXT NOT NULL,
                bet_amount INTEGER DEFAULT 0,
                win_amount INTEGER DEFAULT 0,
                result TEXT,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS ad_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ad_id INTEGER NOT NULL,
                points_earned INTEGER NOT NULL,
                verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(telegram_id)
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS admin_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                target_user INTEGER,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Indexes
        c.execute('CREATE INDEX IF NOT EXISTS idx_users_telegram ON users(telegram_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_users_referral ON users(referral_code)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_spin_history_user ON spin_history(user_id)')

        print("✅ Database initialized!")


def create_user(telegram_id, username, first_name, last_name=None, referred_by=None):
    """Create new user with referral tracking. Returns (referral_code, status_msg)"""
    import random, string
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    with get_db() as conn:
        c = conn.cursor()

        existing = c.execute(
            "SELECT telegram_id FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        if existing:
            return None, "exists"

        try:
            c.execute('''
                INSERT INTO users (telegram_id, username, first_name, last_name,
                                   referral_code, referred_by, points, total_earned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (telegram_id, username, first_name, last_name, code, referred_by,
                  10 if referred_by else 0,
                  10 if referred_by else 0))

            c.execute('''
                INSERT INTO transactions (user_id, type, amount, description)
                VALUES (?, ?, ?, ?)
            ''', (telegram_id, 'welcome_bonus', 10 if referred_by else 0,
                  'Welcome bonus' + (' (referral)' if referred_by else '')))

            if referred_by:
                c.execute('''
                    UPDATE users
                    SET points = points + 50,
                        total_earned = total_earned + 50,
                        total_refs = total_refs + 1
                    WHERE telegram_id = ?
                ''', (referred_by,))

                c.execute('''
                    INSERT INTO transactions (user_id, type, amount, description)
                    VALUES (?, ?, ?, ?)
                ''', (referred_by, 'referral_bonus', 50, f'Referral: {first_name}'))

                c.execute('''
                    INSERT OR IGNORE INTO referral_earnings (referrer_id, referred_id, points_earned)
                    VALUES (?, ?, ?)
                ''', (referred_by, telegram_id, 50))

            return code, "success"

        except Exception as e:
            return None, str(e)


def get_user(telegram_id):
    """Get complete user data as dict"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        return dict(row) if row else None


def update_points(telegram_id, amount, reason, transaction_type='adjustment'):
    """Update user points. Returns (success: bool, new_balance: int)"""
    with get_db() as conn:
        c = conn.cursor()

        current = c.execute(
            "SELECT points FROM users WHERE telegram_id = ?", (telegram_id,)
        ).fetchone()
        if not current:
            return False, 0

        new_balance = current['points'] + amount
        if new_balance < 0:
            return False, current['points']

        if amount > 0:
            c.execute('''
                UPDATE users
                SET points = ?, total_earned = total_earned + ?
                WHERE telegram_id = ?
            ''', (new_balance, amount, telegram_id))
        else:
            c.execute('''
                UPDATE users
                SET points = ?, total_spent = total_spent + ?
                WHERE telegram_id = ?
            ''', (new_balance, abs(amount), telegram_id))

        c.execute('''
            INSERT INTO transactions (user_id, type, amount, balance_after, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, transaction_type, amount, new_balance, reason))

        return True, new_balance


def get_leaderboard(limit=10):
    """Get top users by points"""
    with get_db() as conn:
        rows = conn.execute('''
            SELECT telegram_id, first_name, username, points, total_earned, total_refs
            FROM users WHERE banned = 0
            ORDER BY points DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        return [dict(r) for r in rows]


def get_stats():
    """Get global bot statistics"""
    with get_db() as conn:
        c = conn.cursor()
        pending = c.execute(
            "SELECT COUNT(*), COALESCE(SUM(points), 0) FROM withdrawals WHERE status = 'pending'"
        ).fetchone()
        return {
            'total_users':       c.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            'today_users':       c.execute("SELECT COUNT(*) FROM users WHERE date(created_at) = date('now')").fetchone()[0],
            'total_points':      c.execute("SELECT COALESCE(SUM(points), 0) FROM users").fetchone()[0],
            'total_earned':      c.execute("SELECT COALESCE(SUM(total_earned), 0) FROM users").fetchone()[0],
            'active_today':      c.execute("SELECT COUNT(*) FROM users WHERE date(updated_at) = date('now')").fetchone()[0],
            'pending_count':     pending[0],
            'pending_points':    pending[1],
            'vip_users':         c.execute("SELECT COUNT(*) FROM users WHERE vip_until > datetime('now')").fetchone()[0],
            'spins_today':       c.execute("SELECT COUNT(*) FROM spin_history WHERE date(created_at) = date('now')").fetchone()[0],
        }
