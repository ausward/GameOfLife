package life

import (
	"math/rand"
	"strings"
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
	Starts []func()
}

func NewGameOfLifeGrid(width, height int) *GameOfLifeGrid {

	source := rand.NewSource(time.Now().Unix())
	r := rand.New(source)

	cells := make([][]*GameOfLifeCell, height)
	for i := range cells {
		cells[i] = make([]*GameOfLifeCell, width)
		for j := range cells[i] {
			cells[i][j] = &GameOfLifeCell{X: j, Y: i}
			if r.Int63n(2) == 1 {
				cells[i][j].SetAlive()
			}
		}
	}

	temp := &GameOfLifeGrid{
		width:  width,
		height: height,
		Cells:  cells,
	}
	tempStarts := []func(){}
	tempStarts = append(tempStarts, temp.NewWithCenter)
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("STERLING URGENT CARE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("RESURGENCE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("RESTARTING") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("REGULATING") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("ULCERATING") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("GLISTENING") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("RELUCTANCE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("SULTRINESS") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("INCARNATE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("INCULCATE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("LITIGATES") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("REGULATES") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("RESCALING") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("CELL") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("START") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("RISE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("GENES") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("NUCLEI") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("CULTURE") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("GLINT") })
	tempStarts = append(tempStarts, func() { temp.NewGameLetters("TRUST") })
	tempStarts = append(tempStarts, temp.NewGameRand)
	temp.Starts = tempStarts

	return temp
}

func (g *GameOfLifeGrid) getCell(x, y int) *GameOfLifeCell {
	if x < 0 || x >= g.width || y < 0 || y >= g.height {
		return nil
	}
	return g.Cells[y][x]
}

func (g *GameOfLifeGrid) DoAnIteration() {

	newCells := make([][]*GameOfLifeCell, g.height)
	for row := range newCells {
		newCells[row] = make([]*GameOfLifeCell, g.width)
		for col := range newCells[row] {
			newCells[row][col] = &GameOfLifeCell{X: col, Y: row}
		}
	}
	for row := range g.height {
		for col := range g.width {
			// println("row :", row , "col :", col, g.DoesItLive(row, col))
			newCells[row][col].X = col
			newCells[row][col].Y = row

			if g.DoesItLive(col, row) {
				newCells[row][col].SetAlive()
			} else {
				newCells[row][col].SetDead()
			}
		}

	}

	g.Cells = newCells

}

func (g *GameOfLifeGrid) NewWithCenter() {
	centerH := g.height / 2
	CW := g.width / 2
	newCells := g.newEmpty()
	newCells[centerH+1][CW].SetAlive()
	newCells[centerH][CW].SetAlive()
	newCells[centerH-1][CW].SetAlive()
	newCells[centerH+1][CW+1].SetAlive()
	newCells[centerH][CW-1].SetAlive()
	g.Cells = newCells
}

// Any live cell with fewer than two live neighbours dies, as if by underpopulation.
// Any live cell with two or three live neighbours lives on to the next generation.
// Any live cell with more than three live neighbours dies, as if by overpopulation.
// Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
// _ _ _
// _ X _
// _ _ _
func (g *GameOfLifeGrid) DoesItLive(col, row int) bool {
	// get count of live
	liveNeighbors := 0

	up := -1
	down := 2
	left := -1
	right := 2

	// Corrected border handling for xIndex (column)
	if col == 0 {
		left = 0 // Adjust 'left' bound for cells in the first column
	} else if col == g.width-1 {
		right = 1 // Adjust 'right' bound for cells in the last column
	}

	// Corrected border handling for yIndex (row)
	if row == 0 {
		up = 0 // Adjust 'up' bound for cells in the first row
	} else if row == g.height-1 {
		down = 1 // Adjust 'down' bound for cells in the last row
	}

	for i := up; i < down; i++ {
		for j := left; j < right; j++ {
			if i == 0 && j == 0 {
				continue
			}
			if g.Cells[row+i][col+j].Alive {
				liveNeighbors++
			}
		}
	}

	if !g.getCell(col, row).IsAlive() && liveNeighbors == 3 {
		return true
	}

	if g.getCell(col, row).IsAlive() {
		// Rules for a live cell
		if liveNeighbors < 2 || liveNeighbors > 3 {
			return false // Underpopulation or Overpopulation
		}
		return true // Survival
	} else {
		// Rule for a dead cell
		if liveNeighbors == 3 {
			return true // Reproduction
		}
		return false // Remains dead
	}

}

func (g *GameOfLifeGrid) newEmpty() [][]*GameOfLifeCell {
	newCells := make([][]*GameOfLifeCell, g.height)
	for i := range newCells {
		newCells[i] = make([]*GameOfLifeCell, g.width)
		for j := range newCells[i] {
			newCells[i][j] = &GameOfLifeCell{X: j, Y: i}
		}
	}

	return newCells
}

// same as whats in the iterator
func (g *GameOfLifeGrid) NewGameRand() {
	source := rand.NewSource(time.Now().Unix())
	r := rand.New(source)

	cells := make([][]*GameOfLifeCell, g.height)
	for i := range cells {
		cells[i] = make([]*GameOfLifeCell, g.width)
		for j := range cells[i] {
			cells[i][j] = &GameOfLifeCell{X: j, Y: i}
			if r.Int63n(2) == 1 {
				cells[i][j].SetAlive()
			}
		}
	}

	g.Cells = cells
}

func (g *GameOfLifeGrid) NewGameLetters(message string) {

	centerRow := (g.height / 3)
	centerCol := (g.width / 2) - 25

	newCells := g.newEmpty()

	UpperCase_massage := strings.ToUpper(message)

	for _, r := range UpperCase_massage {

		if r == ' ' {
			centerRow += 7
			centerCol -= 10
			continue
		}

		let, ok := letters[r]
		if !ok {
			g.NewWithCenter()
			return
		}

		for row := range 5 {
			for col := range 3 {
				if let[row][col] {
					newCells[centerRow+row][centerCol+col].SetAlive()
				}
			}
		}

		centerCol += 5
	}

	g.Cells = newCells
}

// slice of functions

// Time For Letters

var letters = map[rune][5][3]bool{
	'S': { // 'S' is the rune key
		{true, true, true},   // This is row 0 (3 boolean values)
		{true, false, false}, // This is row 1
		{true, true, true},   // This is row 2
		{false, false, true}, // This is row 3
		{true, true, true},   // This is row 4
	},
	'T': {
		{true, true, true},
		{false, true, false},
		{false, true, false},
		{false, true, false},
		{false, true, false},
	},
	'E': {
		{true, true, true},
		{true, false, false},
		{true, true, true},
		{true, false, false},
		{true, true, true},
	},
	'R': {
		{true, true, true},
		{true, false, true},
		{true, true, true},
		{true, true, false},
		{true, false, true},
	},
	'L': {
		{true, false, false},
		{true, false, false},
		{true, false, false},
		{true, false, false},
		{true, true, true},
	},
	'I': {
		{true, true, true},
		{false, true, false},
		{false, true, false},
		{false, true, false},
		{true, true, true},
	},
	'N': {
		{true, true, true},
		{true, false, true},
		{true, false, true},
		{true, false, true},
		{true, false, true},
	},
	'G': {
		{false, true, true},
		{true, false, false},
		{true, false, true},
		{true, false, true},
		{false, true, false},
	},
	'U': {
		{true, false, true},
		{true, false, true},
		{true, false, true},
		{true, false, true},
		{false, true, false},
	},
	'C': {
		{false, true, false},
		{true, false, true},
		{true, false, false},
		{true, false, true},
		{false, true, false},
	},
	'A': {
		{false, true, false},
		{true, false, true},
		{true, true, true},
		{true, false, true},
		{true, false, true},
	},
	// ... more characters
	' ': { // The space character
		{false, false, false},
		{false, false, false},
		{false, false, false},
		{false, false, false},
		{false, false, false},
	},
}
