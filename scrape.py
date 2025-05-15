from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
# headless mode
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

try:
    # load the page
    driver.get('https://store.steampowered.com/explore/new/')
    
    # wait for the page to load properly
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tab_item_name"))
    )
    
    # get game information
    games = driver.find_elements(By.CLASS_NAME, "tab_item")
    
    output = []
    for game in games:
        try:
            # get title of games
            title = game.find_element(By.CLASS_NAME, "tab_item_name").text
            # get price of games
            try:
                price = game.find_element(By.CLASS_NAME, "discount_final_price").text
            except:
                price = "Free"
                
            # get tags
            tags = game.find_element(By.CLASS_NAME, "tab_item_top_tags").text.split(", ")
            
            # get platforms
            platforms_div = game.find_element(By.CLASS_NAME, "tab_item_details")
            platform_elements = platforms_div.find_elements(By.CSS_SELECTOR, "span[class*='platform_img']")
            # only want win, mac or linux
            platforms = [p.get_attribute("class").split("platform_img_")[-1] for p in platform_elements]
            # not a platform
            platforms = [p for p in platforms if p != "hmd_separator"]

            output.append({
                'title': title,
                'price': price,
                'tags': tags,
                'platforms': platforms
            })
        except Exception as e:
            print(f"Error processing game: {e}")

    seen_titles = set()

    for game in output:
        # skip if no titles and price
        if not (game.get('title') and game.get('price')):
            continue
        
        if game['title'] in seen_titles:
            continue
        
        seen_titles.add(game['title'])
        
        game_info = {}
        
        if game['title']:
            game_info['Title'] = game['title']
        
        if game['price']:
            game_info['Price'] = game['price']
        
        if game['tags'] and any(game['tags']):
            game_info['Tags'] = ', '.join(game['tags'])
        
        platforms = [p.replace('platform_img_', '').replace('platform_img ', '') for p in game['platforms']]
        platforms = [p for p in platforms if p and p != 'group_separator']
        
        if platforms:
            game_info['Platforms'] = ', '.join(sorted(set(platforms)))
        
        if game_info:
            for key, value in game_info.items():
                print(f"{key}: {value}")
            print("-" * 50)

finally:
    driver.quit()