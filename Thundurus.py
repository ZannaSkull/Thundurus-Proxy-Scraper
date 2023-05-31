from colorama import Fore, Style
from pypresence import Presence
from plyer import notification
from bs4 import BeautifulSoup
import colorama
import requests
import asyncio
import ctypes
import httpx
import os

title = "Thundurus"
title_bytes = title.encode('cp1252') 
ctypes.windll.kernel32.SetConsoleTitleA(title_bytes)

RPC = Presence(client_id="1113456553836691527")
RPC.connect() 
RPC.update(
    state="Thundurus | Proxy scraper",
    details="Made By Hisako",
    large_image="thunduruslarge",
    large_text="Best Proxy Scraper "
)

colorama.init()

ascii_text = r"""
 _____ _                     _                      
/__   \ |__  _   _ _ __   __| |_   _ _ __ _   _ ___ 
  / /\/ '_ \| | | | '_ \ / _` | | | | '__| | | / __|
 / /  | | | | |_| | | | | (_| | |_| | |  | |_| \__ \
 \/   |_| |_|\__,_|_| |_|\__,_|\__,_|_|   \__,_|___/
                                                    
                  Proxy Scraper
                       <3
                 Made By Hisako                   
                                                    
""".format()


async def scrape_proxy(url, proxies):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)

            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, 'html.parser')
                proxy_table = soup.find('table')

                for row in proxy_table.find_all('tr')[1:]:
                    columns = row.find_all('td')
                    ip = columns[0].text
                    port = columns[1].text
                    proxy = f'{ip}:{port}'

                    if ':' in proxy and proxy.count('.') == 3:
                        if proxy not in proxies:
                            proxies.append(proxy)
                            print(Fore.GREEN + f'Success: {proxy}' + Style.RESET_ALL)
                        else:
                            print(Fore.YELLOW + f'Duplicate proxy found: {proxy}. Skipping...' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'Failed to retrieve proxies from {url}. Skipping...' + Style.RESET_ALL)
    except (httpx.HTTPError, httpx.TimeoutException) as e:
        print(Fore.RED + f'An error occurred while scraping {url}: {str(e)}. Skipping...' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'An unexpected error occurred while scraping {url}: {str(e)}. Skipping...' + Style.RESET_ALL)

async def scrape_proxies():
    urls = [
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://www.socks-proxy.net/',
        'https://www.proxynova.com/proxy-server-list/',
        'https://www.proxyscan.io/',
        'https://www.proxy-list.download/',
        'https://www.proxy-listen.de/Proxy/Proxyliste.html',
        'https://www.proxydocker.com/en/proxylist/country/US',
        'https://www.proxyrack.com/proxyfinder/proxies.json',
        'https://www.proxy-list.download/HTTP',
        'https://www.proxyscrape.com/',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=http',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5',
        'https://www.sslproxies24.top/',
        'https://www.proxylists.net/',
        'https://www.proxyserversites.com/',
        'https://www.ipaddress.com/proxy-list/',
        'https://free-proxy-list.net/uk-proxy.html',
        'https://www.proxies24.com/',
        'https://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc',
        'https://www.proxy-list.org/english/index.php',
        'https://www.my-proxy.com/free-proxy-list.html',
        'https://proxydb.net/',
        'https://www.proxynova.com/proxy-server-list/',
        'https://www.proxylisty.com/',
        'https://www.proxyscrape.com/proxies',
        'https://www.proxylistdownload.com/',
        'https://www.proxylists.net/http_highanon.txt',
        'https://www.sslproxies.org/',
        'https://www.proxylists.net/anonymous.html',
        'https://www.freeproxy.world/',
        'https://hidemy.name/en/proxy-list/',
        'https://www.proxy-list.download/SOCKS4',
        'https://www.proxy-list.download/SOCKS5',
        'https://www.proxy-daily.com/',
        'https://www.gatherproxy.com/',
        'https://premproxy.com/',
        'https://www.proxyserverlist24.top/',
        'https://proxies-free.com/',
        'https://www.socks-proxy.net/',
        'https://www.vpnbook.com/freevpn',
        'https://freevpn.us/',
        'https://www.proxy-listen.de/Proxy/Proxyliste.html',
        'https://www.freeproxychecker.com/result/socks4_proxies.txt',
        'https://www.freeproxychecker.com/result/socks5_proxies.txt',
        'https://www.freeproxychecker.com/result/http_proxies.txt',
    ]  
    # You can add more urls
    proxies = []

    tasks = [scrape_proxy(url, proxies) for url in urls]
    await asyncio.gather(*tasks)

    return proxies

async def main():

    notification.notify(
        title='Thundurus',
        message='Proxy scraping started',
        app_icon=None
    )
    
    proxies = await scrape_proxies()

    proxy_type = input('Choose the type of proxies you want (A: Anonymous, T: Transparent, E: Everything): ')

    filtered_proxies = []
    total_count = len(proxies)
    anonymous_count = 0
    transparent_count = 0

    if proxy_type.upper() == 'A':
        filtered_proxies = [proxy for proxy in proxies if 'Anonymous' in proxy]
        anonymous_count = len(filtered_proxies)
        print('Filtered proxies: Anonymous')
    elif proxy_type.upper() == 'T':
        filtered_proxies = [proxy for proxy in proxies if 'Transparent' in proxy]
        transparent_count = len(filtered_proxies)
        print('Filtered proxies: Transparent')
    elif proxy_type.upper() == 'E':
        filtered_proxies = proxies
        anonymous_count = sum('Anonymous' in proxy for proxy in filtered_proxies)
        transparent_count = sum('Transparent' in proxy for proxy in filtered_proxies)
        print('Filtered proxies: Everything')
    else:
        print('Invalid choice. Showing all proxies.')

    for proxy in filtered_proxies:
        if ':' in proxy:
            ip, port = proxy.split(':')[:2]
            proxy = f'{ip}:{port}'

        print(proxy)

    print(Fore.GREEN + f'Total proxies found: {total_count}' + Style.RESET_ALL)
    print(Fore.BLUE + f'Anonymous proxies found: {anonymous_count}' + Style.RESET_ALL)
    print(Fore.YELLOW + f'Transparent proxies found: {transparent_count}' + Style.RESET_ALL)

    save_to_file = input('Do you want to save the proxies to a file? (Y/N): ')
    if save_to_file.lower() == 'y':
        with open('ProxySesso.txt', 'w') as file:
            for proxy in filtered_proxies:
                if ':' in proxy:
                    ip, port = proxy.split(':')[:2]
                    proxy = f'{ip}:{port}'
                    file.write(proxy + '\n')

        print('Proxies saved to ProxySesso.txt')
        notification.notify(
            title='Thundurus',
            message='Proxies saved to file: ProxySesso.txt',
            app_icon=None
        )
    else:
        print('Proxies not saved to a file.')

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.BLUE + ascii_text + Style.RESET_ALL)
    start = input("Do you want to start using the program? (Y/N): ")
    if start.lower() == "y":
        asyncio.run(main())
    else:
        RPC.close()
        print("Goodbye!")

if __name__ == '__main__':
    menu()
