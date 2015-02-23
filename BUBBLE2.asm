	JMP     INIT		;
	DB      "54321"		;
INIT:                   ;
	MOV    	AL,02		;
	MOV	    BL,C0		;
	JMP 	LOAD		;
LOAD:                   ;
	CMP	    AL,07		;
	JZ	    START		;
	MOV	    CL,[AL]		;
	MOV	    [BL],CL		;
	INC	    AL  		;
	INC	    BL	    	;
	JMP	    LOAD		;
START:                  ;
	MOV	    AL,0		; Swap register
	MOV	    BL,0		; Swap register
	MOV	    CL,C0		; Display pointer
	MOV	    DL,0		; Swap counter
	MOV     AL,20		; Move " " to AL
	MOV	    [C5],AL		; Move AL to RAM [C5] (hardcoded for display popup)
	MOV	    AL,0		; Reset AL for program start
MAIN:                   ;
	CMP	    DL,05		; Check for sorting completion (swap counter starts at 0, decrements at each comparison with a swap, increments at each comparison without a swap, value of 5 marks fully sorted with no false positives)
	JZ	    BYE		    ; Exit if list is sorted
	CMP	    CL,C4		; Is the display pointer at the end of the list?
	JZ	    RESET		; If yes, jump to reset label
	MOV	    AL,[CL]		; Move value at display pointer to AL
	INC     CL		    ; Increment display pointer to get next value
	MOV	    BL,[CL]		; Move value at display pointer to BL
	CMP     AL,BL		; Is AL greater than BL?
	JNS	    SWAP		; If yes, jump to swap label
	CMP	    BL,AL		; Is BL greater than AL?
	JNS	    CHECK		; If yes, jump to check label
CHECK:                  ;
	INC	    DL		    ; Increment swap counter
	JMP     MAIN		; Jump back to main loop
SWAP:                   ;
	DEC	    DL		    ; Decrement swap counter
	PUSH    AL		    ; Push value 1 to stack from AL
	PUSH    BL		    ; Push value 2 to stack from BL
	POP	    AL		    ; Pop value 2 from stack to AL
	POP	    BL		    ; Pop value 1 from stack to BL
	DEC	    CL		    ; Decrement display pointer
	MOV	    [CL],AL		; Move AL to [CL]
	INC	    CL		    ; Increment display pointer
	MOV	    [CL],BL		; Move BL to [CL]
	JMP     MAIN	    ; Jump back to main loop
RESET:                  ;
	MOV	    CL,C0		; Reset display pointer to C0
	JMP	    MAIN		; Jump back to main loop
BYE:                    ;
	END			        ; End program