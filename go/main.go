package main

import (
	"image/color"
	"log"

	// "strconv"

	"time"

	"github.com/auswar/GameOfLife/life"

	"github.com/hajimehoshi/ebiten/v2"
	// "github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/vector"
)

const (
	screenHeight int = 900
	screenWidth  int = 1900
)

type Game struct {
	Width      int
	Height     int
	cellSize   int
	life       *life.GameOfLifeGrid
	TIPS       int
	Time       time.Time
	R          int
	G          int
	B          int
	StartIndex int
}

func (g *Game) Update() error {
	ebiten.SetTPS(g.TIPS)
	g.life.DoAnIteration()

	// if (g.R <= 2){g.R,g.G,g.B = 255, 255, 255} else {
	// g.R -= 1
	g.B -= 2
	g.G += 3
	// }
	// if ebiten.IsKeyPressed(ebiten.KeyM) {
	// 	g.life.NewGameLetters("STERLING URGENT CARE")
	// }
	if ebiten.IsKeyPressed(ebiten.KeyN) {
		g.Time = time.Now().Add(-20 * time.Hour)
		
	}

	if ebiten.IsKeyPressed(ebiten.KeyS) && g.TIPS > 1 {
		g.TIPS--
	}
	if ebiten.IsKeyPressed(ebiten.KeyF) {
		g.TIPS++
	}

	if time.Now().After(g.Time.Add(4 * time.Minute)) {
		g.Time = time.Now()
		tempIndex := g.StartIndex
		if g.StartIndex > len(g.life.Starts)-1 {
			tempIndex = 0
			g.StartIndex = 0
		} else {
			g.StartIndex++
		}
		ebiten.SetTPS(1)
		g.life.Starts[tempIndex]()
	}
	// g.TIPS++
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// ebitenutil.DebugPrint(screen, "Hello, World!")

	for _, x := range g.life.Cells {
		for _, y := range x {
			if y.IsAlive() {
				vector.DrawFilledRect(screen, float32(y.X*g.cellSize), float32(y.Y*g.cellSize), float32(g.cellSize), float32(g.cellSize), color.RGBA{uint8(g.R), uint8(g.G), uint8(g.B), 255}, true)
			}

		}

	}

}

func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return g.Width, g.Height
}

func main() {
	// the smaller the size the more the cells
	cellSize := 8

	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Go Way Of Life")
	ebiten.SetWindowResizingMode(ebiten.WindowResizingModeEnabled)
	ebiten.MaximizeWindow()
	ebiten.SetFullscreen(true)
	windowWidth, windowHeight := ebiten.Monitor().Size()
	conn := life.NewGameOfLifeGrid(windowWidth/cellSize, windowHeight/cellSize)
	ebiten.SetWindowSize(windowWidth, windowHeight)
	if err := ebiten.RunGame(&Game{Width: windowWidth, Height: windowHeight, cellSize: cellSize, life: conn, TIPS: 8, Time: time.Now(), R: 255, G: 255, B: 255, StartIndex: 0}); err != nil {
		log.Fatal(err)
	}
}
