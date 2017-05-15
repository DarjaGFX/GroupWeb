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

# Get Post and its Comments{
    {{Domain}}App/PostDetailView/
    POST

    input(string):
        id  #id of Post to get comments,
    
    output(JSON): #this could return a list of output  
        
        Post{
            Title,
            author,
            Text,
            Time,
        }
        Comments{    
            Name,   
            Text,
            Time,
        }
}

# fetch Group names{
    {{Domain}}/App/GroupNames/

    output(JSON):
        Name,
}