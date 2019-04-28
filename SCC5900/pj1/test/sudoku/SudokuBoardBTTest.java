/*
 * Unit tests for creating and filling up a Sudoku board
 * 
 * @author: Damares Resende
 * @contact: damaresresende@usp.br
 * @since: Apr 14, 2019
 * 
 * @organization: University of Sao Paulo (USP)
 *     Institute of Mathematics and Computer Science (ICMC)
 *     Project of Algorithms Class (SCC5000)
*/

package sudoku;

import static org.junit.Assert.*;

import java.io.File;

import org.junit.BeforeClass;
import org.junit.Test;


public class SudokuBoardBTTest {

	public static SudokuBoardBT answer;
	public static String boardFile; 
	
	/**
     * Setting up answer board and board file name
     */
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		boardFile = System.getProperty("user.dir") + File.separator + "test" + File.separator 
				+ "boards" + File.separator + "board1.txt";
		
		String answerFile = System.getProperty("user.dir") + File.separator + "test" + File.separator 
				+ "boards" + File.separator + "board1_answer.txt";
		answer = new SudokuBoardBT(3);
		answer.fillData(answerFile);
	}
	
	/**
     * Tests if board values are set to zero when it is first initialized
     */
	@Test
	public void testBoardInitialization() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		
		for(int i = 0; i < board.getBoardSize(); i++) {
			for (int j = 0; j < board.getBoardSize(); j++) {
				assertEquals(board.getCellValue(i, j), 0);
			}
		}
	}
	
	/**
     * Tests if values are correctly read from board1.txt file
     */
	@Test
	public void testParseBoardValues() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		board.fillData(boardFile);
		
		assertEquals(6, board.getCellValue(0, 1));
		assertEquals(8, board.getCellValue(1, 2));
		assertEquals(2, board.getCellValue(2, 0));
		
		assertEquals(0, board.getCellValue(4, 4));
		
		assertEquals(2, board.getCellValue(6, 8));
		assertEquals(9, board.getCellValue(7, 6));
		assertEquals(7, board.getCellValue(8, 7));
	}

	/**
     * Tests if the evaluation of row constraint is ok
     */
	@Test
	public void testEvaluateRowConstraint() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(0, 0), 6));
		assertTrue(board.evaluate(new Coordinates(0, 2), 3));
	}
	
	/**
     * Tests if the evaluation of column constraint is ok
     */
	@Test
	public void testEvaluateColumnConstraint() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(7, 0), 2));
		assertTrue(board.evaluate(new Coordinates(4, 0), 4));
	}
	
	/**
     * Tests if pivot values are correctly retrieved
     */
	@Test
	public void testSetKernel() {
		Coordinates cell = new Coordinates(7, 0);
		assertEquals(6, cell.getPivotI());
		assertEquals(0, cell.getPivotJ());
		
		cell = new Coordinates(3, 7);
		assertEquals(3, cell.getPivotI());
		assertEquals(6, cell.getPivotJ());
		
		cell = new Coordinates(7, 8);
		assertEquals(6, cell.getPivotI());
		assertEquals(6, cell.getPivotJ());
		
		cell = new Coordinates(0, 0);
		assertEquals(0, cell.getPivotI());
		assertEquals(0, cell.getPivotJ());
		
		cell = new Coordinates(5, 2);
		assertEquals(3, cell.getPivotI());
		assertEquals(0, cell.getPivotJ());
		
		cell = new Coordinates(3, 5);
		assertEquals(3, cell.getPivotI());
		assertEquals(3, cell.getPivotJ());
		
		cell = new Coordinates(8, 3);
		assertEquals(6, cell.getPivotI());
		assertEquals(3, cell.getPivotJ());
		
		cell = new Coordinates(2, 7);
		assertEquals(0, cell.getPivotI());
		assertEquals(6, cell.getPivotJ());
		
		cell = new Coordinates(1, 4);
		assertEquals(0, cell.getPivotI());
		assertEquals(3, cell.getPivotJ());
	}
	
	/**
     * Tests if the evaluation of cell neighborhood square constraint is ok
     */
	@Test
	public void testEvaluateSquareConstraint() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(4, 4), 7));
		assertFalse(board.evaluate(new Coordinates(2, 7), 6));
		assertFalse(board.evaluate(new Coordinates(5, 1), 8));
		assertTrue(board.evaluate(new Coordinates(4, 7), 1));
	}
	
	/**
     * Tests if all values to be filled are filled after backtracking
     */
	@Test
	public void testBacktrackingFullFill() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		
		board.fillData(boardFile);
		board.backtracking(board.getNextCellToFill());
		
		assertTrue(board.toCompleteIsEmpty());
	}
	
	/**
     * Tests if all values to be filled are correctly filled after backtracking
     */
	@Test
	public void testBacktrackingCorrectFill() {
		SudokuBoardBT board = new SudokuBoardBT(3);
		board.fillData(boardFile);
		board.backtracking(board.getNextCellToFill());

		for(int i = 0; i < board.getBoardSize(); i++) {
			for (int j = 0; j < board.getBoardSize(); j++) {
				assertEquals(answer.getCellValue(i, j), board.getCellValue(i, j));
			}
		}
	}
}