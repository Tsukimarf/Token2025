class RightTriangleRenderer {
  /**
   * Render a right triangle onto a canvas element.
   * @param {HTMLCanvasElement} canvas - Target canvas element.
   * @param {number} sideA - Length of base (horizontal).
   * @param {number} sideB - Length of height (vertical).
   * @param {Object} options - Customization parameters.
   */
  static renderToCanvas(canvas, sideA, sideB, options = {}) {
    const {
      padding = 40,
      strokeColor = "#3b82f6",
      fillColor = "rgba(59, 130, 246, 0.15)",
      textColor = "#f8fafc",
      lineWidth = 3,
      showSquare = true
    } = options;

    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;

    // Clear previous renders
    ctx.clearRect(0, 0, width, height);

    // Calculate scaling to fit within canvas margins
    const drawWidth = width - padding * 2;
    const drawHeight = height - padding * 2;
    const scale = Math.min(drawWidth / sideA, drawHeight / sideB);

    const scaledA = sideA * scale;
    const scaledB = sideB * scale;

    // Triangle corner coordinates (Right angle at bottom-left)
    const x0 = padding;
    const y0 = height - padding;           // Bottom-Left (Right angle)
    const x1 = padding + scaledA;
    const y1 = height - padding;           // Bottom-Right
    const x2 = padding;
    const y2 = height - padding - scaledB; // Top-Left

    // Draw Right-Angle Indicator Box
    if (showSquare) {
      const squareSize = Math.min(scaledA, scaledB) * 0.15;
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.rect(x0, y0 - squareSize, squareSize, squareSize);
      ctx.stroke();
    }

    // Draw Main Triangle Shape
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.closePath();

    ctx.fillStyle = fillColor;
    ctx.fill();

    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = lineWidth;
    ctx.stroke();

    // Draw Labels
    const c = Math.sqrt(sideA ** 2 + sideB ** 2);
    ctx.fillStyle = textColor;
    ctx.font = "14px monospace";
    ctx.textAlign = "center";

    // Side A (Base)
    ctx.fillText(`a = ${sideA}`, x0 + scaledA / 2, y0 + 25);
    // Side B (Height)
    ctx.textAlign = "right";
    ctx.fillText(`b = ${sideB}`, x0 - 10, y0 - scaledB / 2);
    // Hypotenuse C
    ctx.textAlign = "left";
    ctx.fillText(`c = ${c.toFixed(2)}`, x0 + scaledA / 2 + 10, y0 - scaledB / 2);
  }

  /**
   * Generates a base64 PNG Data URL string.
   * @returns {string} Image base64 data URL
   */
  static generatePNGDataURL(sideA, sideB, width = 500, height = 500, options = {}) {
    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    this.renderToCanvas(canvas, sideA, sideB, options);
    return canvas.toDataURL("image/png");
  }
}
