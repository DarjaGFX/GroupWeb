#Signup{
    {{Domain}}/signup/
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
}

#Login{
    {{Domain}}/login/
    POST
    
    input(string):
        nuser,
        npass,
    
    output(JSON):
        Status,
        Token (optional),
}