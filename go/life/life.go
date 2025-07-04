package life

import (
	"math/rand"
	"time"
)

type GameOfLifeCell struct {
	Alive bool
	X     int
	Y     int
}

func (g *GameOfLifeCell) IsAlive() bool {
	return g.Alive
}
func (g *GameOfLifeCell) SetAlive() {
	g.Alive = true
}
func (g *GameOfLifeCell) SetDead() {
	g.Alive = false
}




type GameOfLifeGrid struct {
	width  int
	height int
	Cells  [][]*GameOfLifeCell
}

func NewGameOfLifeGrid(width, height int) *GameOfLifeGrid {
	source := rand.NewSource(time.Now().Unix())
	r := rand.New(source)
	// fmt.Print(r.Intn(100))
	
	cells := make([][]*GameOfLifeCell, height)
	for i := range cells {
		cells[i] = make([]*GameOfLifeCell, width)
		for j := range cells[i] {
			cells[i][j] = &GameOfLifeCell{X: j, Y: i}
			if (r.Int63n(500) == 1){
				cells[i][j].SetAlive()
			}
		}
	}
	return &GameOfLifeGrid{
		width:  width,
		height: height,
		Cells:  cells,
	}
}

func (g *GameOfLifeGrid) getCell(x, y int) *GameOfLifeCell{
	if x < 0 || x >= g.width || y < 0 || y >= g.height {
		return nil
	}
	return g.Cells[y][x]
}

func (g *GameOfLifeGrid) DoAnIteration() {
	for  row := range g.height{
		for col :=   range g.width {
			// println("row :", row , "col :", col, g.DoesItLive(row, col))

			if (g.DoesItLive(row,col)){
				g.getCell(row, col).SetAlive()
			} else {
				g.getCell(row,col).SetDead()
			}
		}

	}

}

// Any live cell with fewer than two live neighbours dies, as if by underpopulation.
// Any live cell with two or three live neighbours lives on to the next generation.
// Any live cell with more than three live neighbours dies, as if by overpopulation.
// Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
// _ _ _
// _ X _
// _ _ _
func (g *GameOfLifeGrid) DoesItLive(xIndex, yIndex int) bool{
	// get count of live 
	liveNeighbors :=0

	up := -1
	down := 2
	left := -1
	right := 2

	if (xIndex == 0){
		up = 0
	} else if (xIndex == g.height -1 ){ down =1 }

	if (yIndex ==0){left = 0} else if (yIndex == g.width -1 ){right = 1}
	
	

	for i := up; i < down; i++ {
		for j:=left;j<right;j++{
			if (g.Cells[xIndex+i][yIndex+j].Alive){
			liveNeighbors++
			}
		}
	}

	if (!g.getCell(xIndex, yIndex).IsAlive() && liveNeighbors==3){return true}

	switch liveNeighbors{
		case 0, 1:
			return false;
		case 2, 3:
			return true;
		default:
			return false;
	}

}

