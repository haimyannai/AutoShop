const http = require('http');
const bodyParser = require('body-parser');
const spawn = require("child_process").spawn;
const express = require('express');
const convert = require('iconv-lite');
const path = require("ejs");
const app = express();
const port = 3000;
// https://www.youtube.com/watch?v=6IOrp8HgnJU&t=355s
/////////////////////////////////connection to DB
const sql = require('mssql');
const config = {
        server: 'LAPTOP-VNSLHC31',  //update me
        user: 'Remez',
        password: '123456789',
        database: "BraudeProject",
        dialect: "mssql",
        port: 1433,
        dialectOptions: {
        instanceName: "SQLEXPRESS"
        },
        options:{

            encrypt: false
        }
};

//var conn= new sql.ConnectionPool(config);
var urlencodedParser = bodyParser.urlencoded({ extended: false })
//register view engine
app.set('view engine','ejs');
app.set('views','./public/views');
app.use(express.json({limit: '1mb'}));
app.use(express.static('./public/styleEJS'));
app.use( express.static( "./public/png" ) );
app.use( express.static( "./public/views" ) );
app.use( express.static( "./public/views/partials" ) );

app.get('/',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    res.render('NewHomePage',{title:'Home Page'});
    conn.close();
})

app.get('/new',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    res.render('NewHomePage',{title:'Home Page'});
    conn.close();
})

app.get('/testpage',(req,res)=>{
    res.render('testpage.ejs');
})
app.get('/testdata',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req = new sql.Request(conn);
        req._query('SELECT * FROM AllProds', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               res.json(recordSet[0][1]);
           }

        });
    })
});

app.get('/About',(req,res)=>{
    res.render('About.ejs');
})

app.get('/Products2',(req,res)=>{
    res.render('Products.ejs');
})
app.get('/Products',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req = new sql.Request(conn);
        req._query('SELECT * FROM AllProds', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               res.json(recordSet[0]);
           }

        });
    })
});

app.get('/buy',(req,res)=>{
    res.render('buy.ejs');
})

app.get('/submit',(req,res)=>{
    res.render('submitlst.ejs');
})

app.get('/totalSum',(req,res)=>{
    res.render('TotalSum.ejs');
})

app.get('/totalSum',(req,res)=>{
    res.render('TotalSum.ejs');
})

app.get('/Connect',(req,res)=>{
    res.render('Connect.ejs');
})

app.get('/WhatsNew',(req,res)=>{
    res.render('WhatsNew.ejs');
})

app.post('/SeparationOp',(req,res)=>{
    const pythonProcess = spawn('python',["./Python Files/SeprateScript.py", JSON.stringify(req.body)]);
    pythonProcess.stdout.on('data', (data) => {
        var list = convert.decode(data,"win1255");
        if(list!="0") {
            var y = JSON.parse(list);
            res.json(y);
        }
        else
            res.json("0");
    });
})


//get the basic names of the products
app.get('/basicNames',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req1 = new sql.Request(conn);
        req1._query('SELECT Base_Prod FROM [BraudeProject].[dbo].[AllProds] GROUP BY Base_Prod', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               res.json(recordSet[0]);
           }
        });
    })
});

//get the cost and the webs of the basic products
//get the cost and the webs of the basic products
app.get('/basicNamesCost',(req,res)=>{
    var conn=new sql.ConnectionPool(config);
    var record=conn.connect(function(err){
        if(err)
            throw err;
        var req2=new sql.Request(conn);
        req2._query('SELECT * FROM AllProds',function (err, recordSet){
            if (err) throw err;
            else {
                conn.close();
                res.json(recordSet[0]);
            }
        });
    })
})

app.post('/Pup', urlencodedParser,(req,res)=>{

    const puppeteer = require('puppeteer');
    (async () => {
        const browser = await puppeteer.launch({headless:false});
        const page = await browser.newPage();
        const dovArr = Array();
        switch (req.body.site){
            case "kishurit":
            {
                await page.goto('http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA');
                await autoScroll(page);
                for(const row of req.body.purchaseList){
                    var quantity = row.quantity;
                    var id = 'div'+ '[id="' + row.realName + '"]';
                    const  div = await page.$(id);
                    var quantityIncrease = (await (await div.$('.list_item_show_price')).getProperty('textContent')).toString();
                    if(quantityIncrease.includes('0.5')){
                        quantity = quantity * 2
                    }
                    // if (quantityIncrease.toString().includes('0.5')){
                    // }
                    for(let i=0;i<quantity;i++){
                        await div.$eval('div[class="add_item quantity"]',  el =>{
                        el.click({clickCount:1})
                        });
                    }
                }
                break;
            }// case Kishurit
            case "sultan":
            {
                await page.goto('http://sultan.pricecall.co.il/');
                for(var row of req.body.purchaseList){
                    var id = '[id="' + row.realName + '"]';
                    const  inputField = await page.$(id);
                    await inputField.type(row.quantity.toString())
                 }
                break;
            }// case sultan
            case "dov":
            {
                 await page.goto('https://dovdov.co.il/products/category/yrqwt-32');
                 for(var row of req.body.purchaseList){
                     if(row.link === "https://dovdov.co.il/products/category/yrqwt-32"){
                         const quantity = row.quantity;
                         var id = 'button[id="'+ row.realName +'"]';
                         for(let i=0;i<quantity;i++){
                             await page.click(id);
                             await page.waitForTimeout(1700);
                             await page.waitForSelector('div[class="messages__wrapper"]',{visible:true})
                         }
                     }
                     else{
                        dovArr.push(row);
                     }
                 }
                 await page.waitForTimeout(1000);
                 await page.click('a[class="fl4"]');
                 await page.waitForNavigation();
                 for(var row of dovArr){
                     const quantity = row.quantity;
                     var id = 'button[id="'+ row.realName +'"]';
                     for(let i=0;i<quantity;i++){
                         await page.click(id);
                         await page.waitForTimeout(1000);
                         await page.waitForSelector('div[class="messages__wrapper"]',{visible:true})
                     }
                 }
                 await page.waitForTimeout(1000);
                 await page.click('a[class="cart-block--link__expand"]');
                 await page.waitForNavigation();
                break;
            }// case dov

        }



  // await browser.close();
})();
res.send('Good Pic')
});

//if we get into team page we will go to about page
app.get('/team',(req,res)=>{
    res.redirect('/Products');
})

app.use((req,res)=>{
    res.status(404).render('404');
})


app.listen(port, () => {console.log('Server run');})


async function autoScroll(page){
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}

