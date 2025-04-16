// Liste von Amazon-Links
const amazonLinks = [
    "https://m.media-amazon.com/images/I/51Zymoq7UnL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/61Iz2yy2CKL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71KilybDOoL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81OthjkJBuL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/91bYsX41DVL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71aG+xDKSYL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81QpkIctqPL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/61IBBVJvSDL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71g2ednj0JL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81eB+7+CkUL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/91HHqVTAJQL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81iqZ2HHD-L._AC_SY400_.jpg"
];

// Container für die Kacheln
const gridContainer = document.getElementById("grid-container");

// Dynamisch Kacheln erstellen
amazonLinks.forEach((link, index) => {
    const tile = document.createElement("div");
    tile.className = "tile";

    const img = document.createElement("img");
    img.src = link;
    img.alt = `Amazon Produkt ${index + 1}`;

    const caption = document.createElement("div");
    caption.className = "caption";
    caption.textContent = `Produkt ${index + 1}`;

    tile.appendChild(img);
    tile.appendChild(caption);
    gridContainer.appendChild(tile);
});