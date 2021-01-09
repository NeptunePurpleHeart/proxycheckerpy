import requests
import speedtest
import asyncio
import socks

s = socks.socksocket()

print("Site to check")

check_site = input()
input_data = []
working = {'proxy':[], 'speed':[]}

async def proxy_speed(proxy):
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    speed.results.share()
    results_dict = speed.results.dict()
    down = int(results_dict['download'])/1000000
    uplo = int(results_dict['upload'])/1000000
    working['speed'].append(f"upload:{uplo:.2f} mbit/s, download:{down:.2f} mbit/s, ping:{results_dict['ping']} ms")
    s.close()
    return results_dict

async def check(proxy):
    try:
        requests.get(check_site, proxies={'http':'http://'+proxy})
    except Exception as err:
        print(err)
        return False
    else:
        prox, port = proxy.split(":")
        s.set_proxy(socks.HTTP, prox, port)
        working['proxy'].append(proxy)
        return True
async def main():
    with open("proxy_list.txt", "r") as proxy_list:
        for line in proxy_list:
            input_data.append(line.strip())
        for i in input_data:
            r = await check(i)
            if r == True:
                asyncio.run(proxy_speed(i))
            print(i + " " + "checked")
        with open("result.txt", "w") as result:
            result.write(f"{check_site}\n")
            for i in range(len(working['proxy'])):
                result.write(f"{working['proxy'][i]}: {working['speed'][i]}\n")
    print("Done")

if __name__ == "__main__":
    await main()
