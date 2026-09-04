// Generate base64 Data URL for a 5-12-13 triangle
const pngUrl = RightTriangleRenderer.generatePNGDataURL(5, 12, 600, 600);

// Download as image file automatically
const downloadLink = document.createElement("a");
downloadLink.href = pngUrl;
downloadLink.download = "right_triangle.png";
downloadLink.click();
