Signup{
    POST
    input(string):
        nuser,
        npass,
        nemail,
        ndispn,
        ngroup,
    
    output(JSON):
        Status,
        Message (optional),
        Error (optional),
}

Login{
    POST
    input(string):
        nuser,
        npass,
    
    output(JSON):
        Status,
        Error (optional),
        Token (optional),
}