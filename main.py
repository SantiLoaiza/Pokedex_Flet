import flet as ft

import asyncio
import aiohttp

pokemon_actual = -1
async def main(page: ft.Page):
    page.window_width= 360
    page.window_height = 640
    page.window_resizable = False
    page.padding = 0
    page.fonts= {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.9/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")
    

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
            


    async def evento_get_pokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -= 1
        
        numero = (pokemon_actual%1000)+1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos = f"Number:{numero}\nName: {resultado['name']}\n\nAbilities:"
        for elemento in resultado['abilities']:
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
        datos += f"\n\nHeight: {resultado['height']}"
        texto.value = datos
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url
        await page.update_async()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
            await asyncio.sleep(0.1)
        
    luz_azul = ft.Container(width=35, height=35, left=2.5, top=2.5, bgcolor=ft.colors.BLUE, border_radius=25)
    boton_azul = ft.Stack([
        ft.Container(width=40, height=40, bgcolor=ft.colors.WHITE, border_radius=25),
        luz_azul,
            ]
        )
    items_superior = [
        ft.Container(boton_azul, width=40, height=40),
        ft.Container(width=20, height=20, bgcolor=ft.colors.ORANGE, border_radius=25),
        ft.Container(width=20, height=20, bgcolor=ft.colors.YELLOW, border_radius=25),
        ft.Container(width=20, height=20, bgcolor=ft.colors.GREEN, border_radius=25), 
    ]


    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    imagen = ft.Image(
        src=sprite_url,
        scale=10,
        width=15,
        height=15,
        top=175/2,
        right=275/2,
    )

    stack_central = ft.Stack(
        [
        ft.Container(width=300, height=200, bgcolor=ft.colors.WHITE, border_radius=10),
        ft.Container(width=275, height=175, bgcolor=ft.colors.BLACK, top=12.5, left=12.5),
        imagen,
        ]
    )
    
    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(20, 0),
            ft.canvas.Path.LineTo(0, 25),
            ft.canvas.Path.LineTo(40, 25),
        ],
        paint=ft.Paint(
                style=ft.PaintingStyle.FILL,
            ),
        ),
    ],
    width=40,
    height=25,
    )

    flecha_superior = ft.Container(triangulo, width=40, height=25, on_click=evento_get_pokemon)
    flechas = ft.Column(
        [
            flecha_superior,
            ft.Container(triangulo, width=40, height=25, rotate=ft.Rotate(angle=3.14159), on_click=evento_get_pokemon),
    ]
    )

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=11,
    )

    items_inferior = [
        ft.Container(width=25), #Margen izquierdo
        ft.Container(texto, padding=5, width=200, height=165, bgcolor=ft.colors.GREEN, border_radius=10),
        ft.Container(width=15), #Margen derecho
        ft.Container(flechas, width=40, height=60),
        
    ]


    superior = ft.Container(content=ft.Row(items_superior), width=300, height=40, margin=ft.margin.only(top=20))
    centro = ft.Container(stack_central, width=300, height=200, margin=ft.margin.only(top=20), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=300, height=200, margin=ft.margin.only(top=40))
    
    col = ft.Column(spacing=0, controls=[
        superior, 
        centro, 
        inferior,
        ])
    contenedor = ft.Container(col, width=360, height=640, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blink()

ft.app(target=main)