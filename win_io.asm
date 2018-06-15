global _println
global _scanln
global _cursorUp

extern _GetStdHandle@4
extern _ReadFile@20
extern _WriteFile@20
extern _GetConsoleScreenBufferInfo@8
extern _SetConsoleCursorPosition@8


SECTION .data

    crlf db 0xD, 0xA
    crlf_len equ $-crlf

    stdin dd 0
    stdout dd 0


SECTION .text

; // prints 'length' characters from 'buffer', then CRLF, to stdout
; // returns non-zero for success, or zero if an error occurred
; int __cdecl println(char *buffer, int length);
_println:
    
    push    ebp
    mov     ebp, esp

    cmp dword   [stdout], 0
    jne         __println_write
    call        _init_stdout
    cmp         eax, -1
    je          __println_fail

    __println_write:

    sub         esp, 4
    mov         edx, esp

    push        0 
    push        edx
    push dword  [ebp+12]
    push dword  [ebp+8]
    push dword  [stdout]
    call        _WriteFile@20
    cmp         eax, 0
    je          __println_exit

    push        0
    push        edx
    push        crlf_len
    push        crlf
    push dword  [stdout]
    call        _WriteFile@20
    cmp         eax, 0
    jne         __println_exit

    __println_fail:

    mov     eax, 0

    __println_exit:

    mov     esp, ebp
    pop     ebp
    ret


; // reads 'count' characters from stdin into 'buffer'
; // returns the number of bytes read
; int __cdecl scanln(char *buffer, int count);
_scanln:

    push    ebp
    mov     ebp, esp

    cmp dword   [stdin], 0
    jne         __scanln_read
    call        _init_stdin
    cmp         eax, -1
    je          __scanln_exit

    __scanln_read:

    push dword  0
    mov         edx, esp

    push        0
    push        edx
    push dword  [ebp+12]
    push dword  [ebp+8]
    push dword  [stdin]
    call        _ReadFile@20
    cmp         eax, 0
    je          __scanln_exit

    mov     ecx, [ebp+8]
    add     ecx, [esp]
    sub     ecx, 1

    __scanln_trim_crlf:

    cmp dword   [ecx], 0xD
    je          __scanln_trim_crlf_dotrim
    
    cmp dword   [ecx], 0xA
    je          __scanln_trim_crlf_dotrim

    jmp     __scanln_exit

    __scanln_trim_crlf_dotrim:

    mov dword   [ecx], 0
    dec         ecx
    dec dword   [esp]
    jmp         __scanln_trim_crlf

    __scanln_exit:

    mov     eax, [esp]

    mov     esp, ebp
    pop     ebp
    ret


; // moves the console cursor up 'count' lines. if the cursor's Y coordinate is
; // less than count then it moves to zero.
; // returns non-zero for success, or zero if an error occurred
; int __cdecl cursorUp(int count);
_cursorUp:

    push    ebp
    mov     ebp, esp

    cmp dword   [stdout], 0
    jne         __cursorUp_getCursor
    call        _init_stdout

    cmp     eax, -1 ; INVALID_HANDLE_VALUE
    je      __cursorUp_exit

    __cursorUp_getCursor:

    sub     esp, 22 ; sizeof(CONSOLE_SCREEN_BUFFER_INFO)

    push        esp
    push dword  [stdout]
    call        _GetConsoleScreenBufferInfo@8
    cmp         eax, 0
    je          __cursorUp_exit

    mov         eax, 0x0
    mov         ax, [esp+6]
    
    sub         ax, [ebp+8]
    jns         __cursorUp_setCursor
    
    mov         eax, 0

    __cursorUp_setCursor:

    push word   ax
    push word   0
    push dword  [stdout]
    call         _SetConsoleCursorPosition@8

    __cursorUp_exit:

    mov     esp, ebp
    pop     ebp
    ret


_init_stdout:

    push    ebp
    mov     ebp, esp

    push    -11
    call    _GetStdHandle@4
    mov     [stdout], eax

    mov     esp, ebp
    pop     ebp
    ret


_init_stdin:

    push    ebp
    mov     ebp, esp

    push    -10
    call    _GetStdHandle@4
    mov     [stdin], eax

    mov     esp, ebp
    pop     ebp
    ret
