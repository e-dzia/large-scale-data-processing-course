var db = connect("mongodb://root:toor@mongodb:27017/reddit");

db.createUser(
    {
        "user" : "root",
        "pwd" : "toor",
        "db" : "reddit",
        "roles" : [
            {
                "role" : "root",
                "db" : "reddit"
            }
        ]
    }
);