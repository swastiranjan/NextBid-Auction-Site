function deleteNote(listingId) {
    fetch("/delete-listing", {
        method: "POST",
        body: JSON.stringify({ listingId: listingId})
    }).then((_res) => {
        window.location.href = "/user-listings";
    });
}

