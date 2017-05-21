# Signup{
    {{Domain}}/App/signup/
    POST
    
    input(string):
        nuser(a-z,A-Z,0-9,!@#$,...),
        npass,
        nemail,
        ndispn,
    
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

# Get Post Comments{
    {{Domain}}/App/Comments/get/
    POST

    input(string):
        id  #id of Post to get comments,
    
    output(JSON): #this could return a list of output  
        
        Comments{    
            Name,   
            Text,
            Date,
            Time,
        }
}

# fetch Group names{
    {{Domain}}/App/Group/get/

    output(JSON):
        Groups{
            Name,
            logo,
        }
}

# Add new Group{
    {{Domain}}/App/Group/set/
    
    input(image , string):
        Token,
        pic,
        Name,
        description,

    output(JSON):
        Status,
}

# fetch Group Posts{
    {{Domain}}/App/PostView/
    
    input(string):
        Group,

    output(JSON):
        Posts{
            Id,
            Image,
            Title,
            author,
            Text,
            Date,
            Time,
        }
}

# Add New Post{
    {{Domain}}/App/Post/set/
    
    input(string):
        Token,
        Title,
        Text,
        status,
        Group,
        Image,

    output(JSON):
        status,
}

# Add New Comment{
    {{Domain}}/App/Comments/set/
    
    input(string):
        Token,
        Text,
        PostId,
        
    output(JSON):
        status,
}

# Get user groups{
    {{Domain}}/App/user/groups/get/
    
    input(string):
        Token,
        
    output(JSON):
        Groups[
            Name,
        ]
}