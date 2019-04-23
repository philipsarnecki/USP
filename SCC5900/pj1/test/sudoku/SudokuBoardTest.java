/*
 * Unit tests for creating a Sudoku board
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


public class SudokuBoardTest {

	public static SudokuBoard answer;
	public static String boardFile; 
	
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		boardFile = System.getProperty("user.dir") + File.separator + "test" + File.separator 
				+ "boards" + File.separator + "board1.txt";
		
		String answerFile = System.getProperty("user.dir") + File.separator + "test" + File.separator 
				+ "boards" + File.separator + "board1_answer.txt";
		answer = new SudokuBoard();
		answer.fillData(answerFile);
	}
	
	@Test
	public void testBoardInitialization() {
		SudokuBoard board = new SudokuBoard();
		
		for(int i = 0; i < board.boardSize; i++) {
			for (int j = 0; j < board.boardSize; j++) {
				assertEquals(board.board[i][j], 0);
			}
		}
	}
	
	@Test
	public void testParseBoardValues() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		
		assertEquals(6, board.board[0][1]);
		assertEquals(8, board.board[1][2]);
		assertEquals(2, board.board[2][0]);
		
		assertEquals(-1, board.board[4][4]);
		
		assertEquals(2, board.board[6][8]);
		assertEquals(9, board.board[7][6]);
		assertEquals(7, board.board[8][7]);
	}

	@Test
	public void testEvaluateRowConstraint() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(0, 0), 6));
		assertTrue(board.evaluate(new Coordinates(0, 2), 3));
	}
	
	@Test
	public void testEvaluateColumnConstraint() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(7, 0), 2));
		assertTrue(board.evaluate(new Coordinates(4, 0), 4));
	}
	
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
	
	@Test
	public void testEvaluateSquareConstraint() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		
		assertFalse(board.evaluate(new Coordinates(4, 4), 7));
		assertFalse(board.evaluate(new Coordinates(2, 7), 6));
		assertFalse(board.evaluate(new Coordinates(5, 1), 8));
		assertTrue(board.evaluate(new Coordinates(4, 7), 1));
	}
	
	@Test
	public void testBacktrackingFullFill() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		
		board.backtracking(board.toComplete.poll());
		assertTrue(board.toCompleteIsEmpty());
	}
	
	@Test
	public void testBacktrackingCorrectFill() {
		SudokuBoard board = new SudokuBoard();
		board.fillData(boardFile);
		board.backtracking(board.toComplete.poll());

		int error = 0;
		for(int i = 0; i < board.boardSize; i++) {
			for (int j = 0; j < board.boardSize; j++) {
//				assertEquals(answer.board[i][j], board.board[i][j]);
				if (answer.board[i][j] != board.board[i][j]) {
					System.out.println("Error in cell " + i + ", " + j + ". " + answer.board[i][j] + " != " + board.board[i][j]);
					error++;
				}
			}
		}
		
		System.out.println("Errors: " + error);
	}
}