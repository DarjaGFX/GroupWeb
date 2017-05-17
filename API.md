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
    {{Domain}}App/Group/load/

    output(JSON):
        Groups{
            Name,
            logo,
        }
}

# Add new Group{
    {{Domain}}App/Group/add/
    
    input(image , string):
        pic,
        Name,
        description,

    output(JSON):
        Status,
}