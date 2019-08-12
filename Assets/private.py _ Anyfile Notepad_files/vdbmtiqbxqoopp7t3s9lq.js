var PREBID_TIMEOUT = 2200;

//viewport width for responsive ads

var PBSClientWidth = 992;
if (document.documentElement.clientWidth > 0) {
    PBSClientWidth = document.documentElement.clientWidth;
}

var adUnits = [];

adUnits.push({"code":"banner-728x90-1","mediaTypes":{"banner":{"sizes":[[728,90]]}},"bids":[{"bidder":"lockerdome","params":{"adUnitId":"LD11919137857565542","accountId":"LD11887731211222272"}},{"bidder":"pulsepoint","params":{"cf":"728X90","cp":"560310","ct":"495689"}},{"bidder":"admedia","params":{"aid":"87180"}}]});
adUnits.push({"code":"banner-120x600-1","mediaTypes":{"banner":{"sizes":[[120,600]]}},"bids":[{"bidder":"pulsepoint","params":{"cf":"120X600","cp":"560310","ct":"561803"}},{"bidder":"admedia","params":{"aid":"87180"}}]});
adUnits.push({"code":"banner-160x600-1","mediaTypes":{"banner":{"sizes":[[160,600]]}},"bids":[{"bidder":"pulsepoint","params":{"cf":"160X600","cp":"560310","ct":"495678"}},{"bidder":"admedia","params":{"aid":"87180"}}]});
adUnits.push({"code":"banner-480x320-1","mediaTypes":{"banner":{"sizes":[[480,320]]}},"bids":[{"bidder":"admedia","params":{"aid":"87180"}}]});

var pbjs = pbjs || {};
pbjs.que = pbjs.que || [];

pbjs.que.push(function () {
    //reference sekindo as appnexus
    pbjs.aliasBidder('appnexus', 'sekindo');
    pbjs.aliasBidder('appnexus', 'districtm');
    pbjs.setConfig({
        priceGranularity: "dense",
        enableSendAllBids: false
    });
});

var googletag = googletag || {};
googletag.cmd = googletag.cmd || [];
googletag.cmd.push(function () {
    googletag.pubads().disableInitialLoad();
});

pbjs.que.push(function () {
    pbjs.addAdUnits(adUnits);
    pbjs.requestBids({
        bidsBackHandler: initAdserver,
        timeout: PREBID_TIMEOUT
    });
});

//only for partners who return bids Gross rather than Net
pbjs.bidderSettings = {
    springserve: {
        bidCpmAdjustment: function (bidCpm) {
            return bidCpm * 0.8;
        }
    },
    brealtime: {
        bidCpmAdjustment: function (bidCpm) {
            return bidCpm * 0.8;
        }
    },
    aol: {
        bidCpmAdjustment: function (bidCpm) {
            return bidCpm * 0.8;
        }
    },
    districtm: {
        bidCpmAdjustment: function (bidCpm) {
            return bidCpm * 0.85;
        }
    }
};

function initAdserver() {
        if (pbjs.initAdserverSet) return;
        pbjs.initAdserverSet = true;
        googletag.cmd.push(function() {
            pbjs.que.push(function() {
                pbjs.setTargetingForGPTAsync();
            googletag.pubads().refresh();
        });
    });
}

setTimeout(function () {
    initAdserver();
}, PREBID_TIMEOUT);