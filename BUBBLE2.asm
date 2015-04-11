	JMP     INIT        ;
	DB      "7936321973296732.";
INIT:                   ;
	MOV        AL,0002        ;
	MOV        BL,FC00        ;
	JMP     LOAD        ;
LOAD:                   ;
	MOV     CL,[AL]        ;
	CMP     CL,002E       ;
	JZ      START       ;
	MOV        [BL],CL        ;
	INC        AL          ;
	INC        BL            ;
	JMP        LOAD        ;
START:                  ;
	DEC     BL          ;
	MOV     [0B00],BL     ;
	MOV        AL,0000        ; Swap register
	MOV        BL,0000        ; Swap register
	MOV        CL,FC00        ; Display pointer
	MOV        DL,0000        ; Swap counter
MAIN:                   ;
	MOV     AL,[0B00]     ;
	SUB     AL,FC00       ;
	CMP        DL,AL        ; Check for sorting completion (swap counter starts at 0, decrements at each comparison with a swap, increments at each comparison without a swap, value of 5 marks fully sorted with no false positives)
	JZ        BYE            ; Exit if list is sorted
	CMP        CL,[0B00]        ; Is the display pointer at the end of the list?
	JZ        RESET        ; If yes, jump to reset label
	MOV        AL,[CL]        ; Move value at display pointer to AL
	INC     CL            ; Increment display pointer to get next value
	MOV        BL,[CL]        ; Move value at display pointer to BL
	CMP     AL,BL        ; Is AL greater than BL?
	JNS        SWAP        ; If yes, jump to swap label
	CMP        BL,AL        ; Is BL greater than AL?
	JNS        CHECK        ; If yes, jump to check label
CHECK:                  ;
	INC        DL            ; Increment swap counter
	JMP     MAIN        ; Jump back to main loop
SWAP:                   ;
	DEC        DL            ; Decrement swap counter
	PUSH    AL            ; Push value 1 to stack from AL
	PUSH    BL            ; Push value 2 to stack from BL
	POP        AL            ; Pop value 2 from stack to AL
	POP        BL            ; Pop value 1 from stack to BL
	DEC        CL            ; Decrement display pointer
	MOV        [CL],AL        ; Move AL to [CL]
	INC        CL            ; Increment display pointer
	MOV        [CL],BL        ; Move BL to [CL]
	JMP     MAIN        ; Jump back to main loop
RESET:                  ;
	MOV        CL,FC00        ; Reset display pointer to C0
	JMP        MAIN        ; Jump back to main loop
BYE:                    ;
	MOV     CL,FC00     ; Re-initialize display pointer
PRINT:                  ;
	CMP     [CL],002E   ; Is CL at a period (end of list delimiter)?
	JZ      EXIT        ; If yes, exit program
	OUT     [CL]        ; If no, output character at [CL] to stdout
	INC     CL          ;
	JMP     PRINT         ;
EXIT:                   ;
	END                    ; End program