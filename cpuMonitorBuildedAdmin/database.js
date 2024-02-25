const { MongoClient, ServerApiVersion } =require('mongodb');

const uri = "mongodb+srv://SUBHAM:MONGODB123@subham.h15frqq.mongodb.net/?retryWrites=true&w=majority"

const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
}); 

const connectToMongoDB = async (req, res, next) => {
    try {
        await client.connect();
        req.dbClient = client;
        req.database = client.db("subham"); 
        next();
    } catch (err) {
        console.error('Error connecting to MongoDB: ', err);
        res.status(500).send('Database connection error');
    }
};

const closeMongoDB = (req, res, next) => {
    if (req.dbClient) {
      req.dbClient.close();
    }
    next();
};

module.exports= {
  closeMongoDB,
  connectToMongoDB
};


