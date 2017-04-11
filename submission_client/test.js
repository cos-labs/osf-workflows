function one() {
    
    console.log('one called');
    return 1;
}

console.log(setTimeout(one, function() {
    console.log('async')
}), 200)

