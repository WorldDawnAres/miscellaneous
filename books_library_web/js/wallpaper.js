let currentIndex = 0;
const wallpaperContainer = document.getElementById('wallpaperImages');
const wallpapers = document.querySelectorAll('#wallpaperImages img');
const totalWallpapers = wallpapers.length;

const firstClone = wallpapers[0].cloneNode(true);
wallpaperContainer.appendChild(firstClone);

let autoScrollInterval = setInterval(() => {
    changeWallpaper(1);
}, 4000);

function changeWallpaper(direction) {
    clearInterval(autoScrollInterval);

    currentIndex += direction;

    wallpaperContainer.style.transition = 'transform 1s ease';
    wallpaperContainer.style.transform = `translateX(-${currentIndex * 100}vw)`;
    if (currentIndex >= totalWallpapers) {
        setTimeout(() => {
            wallpaperContainer.style.transition = 'none';
            currentIndex = 0;
            wallpaperContainer.style.transform = `translateX(0vw)`;

            setTimeout(() => {
                wallpaperContainer.style.transition = 'transform 1s ease';
            }, 50);
        }, 1000);
    } else if (currentIndex < 0) {
        currentIndex = totalWallpapers - 1;
        wallpaperContainer.style.transform = `translateX(-${currentIndex * 100}vw)`;
    }

    autoScrollInterval = setInterval(() => {
        changeWallpaper(1);
    }, 4000);
}

window.onload = function () {
    wallpaperContainer.style.width = `${(totalWallpapers + 1) * 100}vw`;
};
