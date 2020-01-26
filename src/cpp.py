

def ast_to_cpp(ast) -> str:
    return """
    #include <stdio.h>
    
    int main(int argc, char** argv) {
        printf("Hello world!\\n");
        return 0;
    }
    """
