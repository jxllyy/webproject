// Liste von Amazon-Links
const amazonLinks = [
    "https://m.media-amazon.com/images/I/61s4tTAizUL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/41FYkVPzrIL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/51CjYz4iQHL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/61Iz2yy2CKL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71KilybDOoL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81OthjkJBuL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/91bYsX41DVL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71aG+xDKSYL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81QpkIctqPL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/61IBBVJvSDL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/71g2ednj0JL._AC_SY400_.jpg",
    "https://m.media-amazon.com/images/I/81eB+7+CkUL._AC_SY400_.jpg"
];


// Container für die Kacheln
const gridContainer = document.getElementById("grid-container");

// Funktion, um Vorschaubilder von der API abzurufen
async function fetchProductData(productUrl) {
    const asin = productUrl.split("/dp/")[1]; // ASIN aus der URL extrahieren
    const apiUrl = `https://api.example.com/getProduct?asin=${asin}`; // Beispiel-API-URL

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        return data.image; // Vorschaubild-URL aus der API-Antwort
    } catch (error) {
        console.error("Fehler beim Abrufen der Produktdaten:", error);
        return null;
    }
}

// Dynamisch Kacheln erstellen
amazonLinks.forEach(async (link, index) => {
    const tile = document.createElement("div");
    tile.className = "tile";

    const img = document.createElement("img");
    const imageUrl = await fetchProductData(link); // Vorschaubild abrufen
    img.src = imageUrl || "fallback-image.jpg"; // Fallback-Bild, falls kein Bild gefunden wird
    img.alt = `Amazon Produkt ${index + 1}`;

    const caption = document.createElement("div");
    caption.className = "caption";
    caption.textContent = `Produkt ${index + 1}`;

    tile.appendChild(img);
    tile.appendChild(caption);
    gridContainer.appendChild(tile);
});