typedef int (*WriteConsoleAPtr)(void*, const char*, unsigned long, unsigned long*, void*);

long strlen(char *s) {
    long len = 0;
    while (s[len] != 0) len++;
    return len;
}

int main() {
    char *message = "Hello, world!\n";
    long len = strlen(message);
    long written;

    // Function pointers
    void* (*get_module_handle)(const char*) = 0;
    void* (*get_proc_address)(void*, const char*) = 0;
    void* kernel32;

    // Get kernel32.dll handle
    __asm__ (
        "pushl $0\n"
        "call _GetModuleHandleA@4\n"
        "movl %%eax, %0\n"
        : "=r" (kernel32)
        :
        : "eax", "ecx", "edx"
    );

    // Get GetProcAddress
    __asm__ (
        "pushl $0x73734163\n" // "Address" (4 bytes)
        "pushl $0x6f725065\n" // "Proc" (4 bytes)
        "pushl $0x746567\n"   // "Get" (3 bytes, null-terminated)
        "pushl %%esp\n"
        "pushl %1\n"
        "call _GetProcAddress@8\n"
        "movl %%eax, %0\n"
        : "=r" (get_proc_address)
        : "r" (kernel32)
        : "eax", "ecx", "edx", "cc"
    );

    // Get WriteConsoleA
    WriteConsoleAPtr write_console;
    __asm__ (
        "pushl $0x416568\n"   // "ConsoleA" (partial, 3 bytes)
        "pushl $0x74697257\n" // "Write" (4 bytes)
        "pushl %%esp\n"
        "pushl %1\n"
        "call *%2\n"
        "movl %%eax, %0\n"
        : "=r" (write_console)
        : "r" (kernel32), "r" (get_proc_address)
        : "eax", "ecx", "edx", "cc"
    );

    // Call WriteConsoleA
    write_console((void*)-11, message, len, &written, 0);
    return 0;
}