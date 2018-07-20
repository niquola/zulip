angular.module('digest', [])
    .controller('DigestCtl', function($http) {
        var m = this;
        m.title = 'Digest'

        $http.get('/digest/data').then((resp)=>{
            console.log('data', resp.data);
            m.data = resp.data;
        });
        return m;
    });
