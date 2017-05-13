# Signup{
    {{Domain}}/App/signup/
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

# Login{
    {{Domain}}/App/login/
    POST
    
    input(string):
        nuser,
        npass,
    
    output(JSON):
        Status,
        Token (optional),
}

# Get Comments of Specific Post{
    {{Domain}}/App/postComments/
    POST

    input(string):
        id  #id of Post to get comments,
    
    output(JSON): #this could return a list of output  
        Name,   
        Text,
        Time,
}