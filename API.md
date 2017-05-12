Signup{
    POST
    input:
        nuser   : string,
        npass   : string,
        nemail  : string,
        ndispn  : string,
        ngroup  : string,
    
    output(JSON):
        Status,
        Message (optional),
        Error (optional),
}

Login{
    POST
    input:
        nuser:string,
        npass:string,
    
    output(JSON):
        Status,
        Error (optional),
        Token (optional),
}