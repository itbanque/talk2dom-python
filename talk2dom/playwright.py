from .client import Talk2DomClient


async def click(page, instruction: str, client: Talk2DomClient):
    html = await page.content()
    res = await client.alocate(instruction, html=html, url=page.url)
    await page.locator(res.selector_value).click()


async def t2d_fill(page, instruction: str, text: str, client: Talk2DomClient):
    html = await page.content()
    res = await client.alocate(instruction, html=html, url=page.url)
    await page.locator(res.selector_value).fill(text)
