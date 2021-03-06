# queue
An implementation of a [queue](http://en.wikipedia.org/wiki/Queue_(abstract_data_type)), which, in reality, is just a
wrapper for the singly-linked list implemented in `../singly_linked_list/`. `src/queue.c` defines the data-structure
and functions used to manipulate and interact with it, and is designed for easy inclusion in any other C file; its
methods rely on `void` pointers, and are thus generalized for any arbitrary data-type. `src/test.c` contains a
main-block and function calls to test everything inside `queue.c`: some diagnostic messages will be printed at runtime.

 * `make` : Compile the project.
 * `make run` : Run the compiled executable.
 * `make clean` : Remove any compiled files

An example of using the API defined by `queue.c` in another C file:

```c
#include <stdlib.h>
#include <string.h>

#include "queue.h"

static void freeData(void *data){
	free((char *)data);
}

int main(){
	Queue_t *queue = createQueue(freeData);
	char *string = malloc(11);
	strcpy(string, "0xdeadbeef");
	enqueue(queue, string);
	printQueue(queue, "%s\n");
	freeQueue(queue);
	return 0;
}
```
