#Signup{
    {{Domain}}/blog/signup/
    POST
    
    input(string):
        nuser(a-z,A-Z,0-9,!@#$,...),
        npass,
        nemail,
        ndispn,
        ngroup,
    
    output(JSON):
        Status,
        Message (optional),
        Error (optional),
}

#Login{
    {{Domain}}/blog/login/
    POST
    
    input(string):
        nuser,
        npass,
    
    output(JSON):
        Status,
        Error (optional),
        Token (optional),
}