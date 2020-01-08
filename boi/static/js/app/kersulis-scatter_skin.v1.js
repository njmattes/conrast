(function(size, number, timer, threshold, network, cg) {
  'use strict';

  let mode = {
    'g': 'gpxl',
    'c': 'cpxl',
  }[cg];

  let width = window.innerWidth;
  let height = window.innerHeight;

  /**
   * Padding multiplier
   * @type {number}
   */
  const padding_m = 0;

  /**
   * Padding surrounding artwork
   * @type {{top: number, left: number, bottom: number, right: number}}
   */
  const padding = {
    top: size * padding_m,
    right: size * padding_m,
    bottom: size * padding_m,
    left: size * padding_m};
  width = Math.ceil(width / size) - (padding.left + padding.right) / size;
  height = Math.ceil(height / size) - (padding.top + padding.bottom) / size;

  const canvas = d3
    .select('main')
    .append('canvas')
    .attr('width', width * size)
    .attr('height', height * size);
  const ctx = canvas.node().getContext('2d');
  ctx.LineCap = 'round';

  function pxls(t) {
    /**
     * If we have run through all pixels, set t back to 0, begin running
     * the wipe() function, and return.
     */
    if (t >= width * height) {
      t = 0;
      wipe(t);
      return;
    }
    d3.json(`/get_${mode}/${t},${number}/${threshold}/${network}`, {
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      }}).then(json => {
        for (let i = 0; i < json['pxls'].length; ++i) {
          let r = json.pxls[i].color[0];
          let g = json.pxls[i].color[1];
          let b = json.pxls[i].color[2];
          ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 1)`;
          ctx.beginPath();
          ctx.rect(json.pxls[i].xy[0] * size, json.pxls[i].xy[1] * size, size, size);
          ctx.fill();
        }
      });
    t += number;
    setTimeout(pxls.bind({}, t), timer);
  }

  function wipe(t) {

  }

  d3.json(`/init/${width}/${height}`,
    {
      headers: {'Content-type': 'application/json; charset=UTF-8'}
    }).then(json => {
      console.log('db initialized');
      pxls(0);
    });

})(size, number, timer, threshold, network, cg);