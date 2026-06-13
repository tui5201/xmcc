const products = [{id: 1, name: '茶1'}, {id: 2, name: '茶2'}];
const strId = '1';
const numId = parseInt(strId);
console.log('strId:', strId, typeof strId);
console.log('numId:', numId, typeof numId);
console.log('find with strId:', products.find(p => p.id === strId));
console.log('find with numId:', products.find(p => p.id === numId));
