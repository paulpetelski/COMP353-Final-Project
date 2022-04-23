
const isbns = ['9780006174554','9780593188156', '9780531071397'];

for(const book of isbns){
    console.log(book);
    getBook(book);
}

async function getBook(isbn){
    const url = `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`;
    const resp = await fetch(url);
    const data = await resp.json();
    console.log(data);
    
    const book = new Object();
    book.title = data.items[0].volumeInfo.title;
    book.description = data.items[0].volumeInfo.description;
    console.log(book.title);
    console.log(book.description);
}    

console.log(booklist);