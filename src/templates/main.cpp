{%for path in includes%}
#include {{path}}
{%endfor%}

{%for name in predef_classes%}
class {{name}};
{%endfor%}

{%for func in predef_funcs%}
{{func}};
{%endfor%}

int main(int argc, char** argv) {
    std::cout << "Hello world!" << std::endl;
    return 0;
}