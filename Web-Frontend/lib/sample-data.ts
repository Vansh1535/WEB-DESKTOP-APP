export const SAMPLE_CSV_DATA = `Equipment Name,Type,Flowrate,Pressure,Temperature
Centrifugal Pump A,Pump,150.5,8.2,45.3
Centrifugal Pump B,Pump,145.2,7.9,44.8
Positive Displacement Pump,Pump,120.8,12.5,52.1
Rotary Compressor,Compressor,85.3,6.5,38.2
Reciprocating Compressor,Compressor,92.1,7.2,41.5
Screw Compressor,Compressor,110.4,8.1,43.9
Heat Exchanger 1,Heat Exchanger,200.3,3.2,65.4
Heat Exchanger 2,Heat Exchanger,185.7,3.0,62.1
Plate Heat Exchanger,Heat Exchanger,220.5,2.8,68.2
Shell Tube Exchanger,Heat Exchanger,195.2,3.5,64.8
Distillation Column,Reactor,75.2,1.2,78.5
Reactor Vessel,Reactor,65.8,2.1,82.3
Fermenter,Reactor,88.4,1.5,80.1
Crystallizer,Reactor,72.5,1.8,79.6
Vacuum Pump A,Pump,45.2,0.1,22.3
Vacuum Pump B,Pump,38.6,0.08,21.1
Booster Pump,Pump,165.3,15.2,48.2
Submersible Pump,Pump,128.5,5.8,35.4
Gear Pump,Pump,95.3,9.5,46.7
Peristaltic Pump,Pump,35.8,2.2,28.5
Rotary Vane Pump,Pump,55.4,4.1,32.6
Turbine Compressor,Compressor,125.6,9.8,47.2
Centrifugal Compressor,Compressor,105.2,8.3,42.1
Diaphragm Compressor,Compressor,42.3,5.5,36.8
Piston Compressor,Compressor,75.8,10.2,50.3
Scroll Compressor,Compressor,68.4,7.1,39.5
Spiral Plate HE,Heat Exchanger,210.3,2.9,66.1
Finned Tube HE,Heat Exchanger,175.5,3.8,61.5
Double Pipe HE,Heat Exchanger,158.2,4.2,59.3
Brazed Plate HE,Heat Exchanger,225.6,2.5,69.4`;

export function downloadSampleCSV() {
  const blob = new Blob([SAMPLE_CSV_DATA], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'sample_equipment_data.csv';
  link.click();
  window.URL.revokeObjectURL(url);
}

export function parseSampleData() {
  const lines = SAMPLE_CSV_DATA.trim().split('\n');
  const headers = lines[0].split(',').map((h) => h.trim().toLowerCase());
  const data = lines.slice(1).map((line) => {
    const values = line.split(',').map((v) => v.trim());
    const obj: any = {};
    headers.forEach((header, index) => {
      obj[header] = values[index] || '';
    });
    return obj;
  });
  return data;
}
