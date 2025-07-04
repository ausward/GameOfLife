package main

import (
	"image/color"
	"log"

	// "strconv"

	// "time"

	"github.com/auswar/GameOfLife/life"

	"github.com/hajimehoshi/ebiten/v2"
	// "github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/vector"
)

const (
	screenHeight int = 800
	screenWidth  int = 800
)

type Game struct {
	Width    int
	Height   int
	cellSize int
	life     *life.GameOfLifeGrid
}

func (g *Game) Update() error {
	// time.Sleep(1 * time.Second)
	g.life.DoAnIteration()
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// ebitenutil.DebugPrint(screen, "Hello, World!")
	
	for _, x := range g.life.Cells {
		for _, y := range x {
			if y.IsAlive() {
				vector.DrawFilledRect(screen, float32(y.X*g.cellSize), float32(y.Y*g.cellSize), float32(g.cellSize), float32(g.cellSize), color.RGBA{255, 255, 255, 255}, true)
			}

		}

	}

}

func (g *Game) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return g.Width, g.Height
}

func main() {
	cellSize := 1
	conn := life.NewGameOfLifeGrid(800/cellSize, 800/cellSize)
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Hello, World!")
	ebiten.NewImage(100, 100).Fill(color.White)
	ebiten.SetTPS(10)	
	// ebiten.SetVsyncEnabled(false)
	if err := ebiten.RunGame(&Game{Width: 800, Height: 800, cellSize: cellSize, life: conn}); err != nil {
		log.Fatal(err)
	}
}
