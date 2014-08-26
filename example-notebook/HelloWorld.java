import java.util.*;

class HelloWorld {

/* START SOLUTION */

static String helloWorld(String input) {
	// The answer is always:
	return "Hello World!";
}

/* END SOLUTION */

/**
 * This problem requires us to print "Hello World!" on a line for each
 * line of input.
 */
public static void main(String[] args) {
	Scanner in = new Scanner(System.in);

	while (in.hasNextLine()) {
		System.out.println(helloWorld(in.nextLine()));
	}
}
}
