import FileSaver from 'file-saver';

export default function saveJsonToFile(dataToSave, filename) {
  const content = JSON.stringify(dataToSave, null, 2);
  const blob = new Blob([content], {type: 'text/plain;charset=utf-8'});
  FileSaver.saveAs(blob, filename + '.json');
}
