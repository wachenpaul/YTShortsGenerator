import asyncio
from pyppeteer import launch

import nest_asyncio
nest_asyncio.apply()

import json

cookie_modal_class = '.trdUvQxqQHHqQKOUBcgnr'
num_comments = 2
darkMode = True

async def removeClutter(p):
    await p.evaluate('''() => {
        try {document.querySelector('%s').parentNode.removeChild(document.querySelector('%s'))} catch(e) {}
        try {document.querySelector('header').parentNode.innerHTML = ''} catch(e) {}
    }''' % (cookie_modal_class, cookie_modal_class))
        
async def getText(p):
    data = await p.evaluate('''
                     () => {
                             comments1 = document.querySelectorAll('._1ump7uMrSA43cqok14tPrG > div > div > div > div > div[style="padding-left:16px"]')
                             comments2 = [] // document.querySelectorAll('._1ump7uMrSA43cqok14tPrG > div > div > div > div > div[style="padding-left:37px"]')
                             comments = [...comments1, ...comments2].slice(%s)
                             text = []
                             comments.forEach(comment => {
                                 temp = comment.querySelectorAll('.Comment p')
                                 temp2 = []
                                 temp.forEach(e => {
                                     temp2.push(e.innerText)
                                 })
                                 text.push(temp2.join('\\n\\n'))
                            })
                            return text
                           }
                     ''' % num_comments)
    return data

async def getScreenshots():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto("https://www.reddit.com")
    await page.evaluate('() => {window.sessionStorage.setItem("test", "bla")}')
    # await page.goto('https://www.reddit.com/')
    if darkMode: await page.setCookie({'name': 'USER', 'domain': '.reddit.com', 'value': 'eyJwcmVmcyI6eyJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6MCwiZ2xvYmFsVGhlbWUiOiJSRURESVQiLCJuaWdodG1vZGUiOnRydWUsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sInRvcENvbnRlbnRUaW1lc0Rpc21pc3NlZCI6MH19'})
    
    await page.goto('https://www.reddit.com/r/AskReddit/comments/w4uxui/if_you_could_have_any_rare_no_longer_available/')
    
    await removeClutter(page)
    txt = await getText(page)
        
    heading = await page.J('[data-testid="post-container"]')
    comments = await page.JJ('._1ump7uMrSA43cqok14tPrG > div > div > div > div > div[style="padding-left:16px"]')
    comments = comments + await page.JJ('._1ump7uMrSA43cqok14tPrG > div > div > div > div > div[style="padding-left:37px"]')
    
    await heading.screenshot({'path':'heading.png'})
    
    for i, comment in enumerate(comments[:num_comments]):
        await comment.screenshot({'path': f'comment{i}.png'})
    await browser.close()
    return txt
    
text = asyncio.run(getScreenshots())

''' Hier ein Snippet für Bilder Overlay über das Video:
    
    import cv2
    import os
    
    image_folder = 'images'
    video_name = 'video.avi'
    each_image_duration = 5 # in secs
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # define the video codec
    
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    video = cv2.VideoWriter(video_name, fourcc, 1.0, (width, height))
    
    for image in images:
        for _ in range(each_image_duration):
            video.write(cv2.imread(os.path.join(image_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()

'''
