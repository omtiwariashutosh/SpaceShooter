document.addEventListener("keydown", function (event) {
  if (event.key === "ArrowLeft") {
    console.log("Move Left");
  }
  if (event.key === "ArrowRight") {
    console.log("Move Right");
  }
  if (event.key === " ") {
    console.log("Shoot Bullet");
  }
});
