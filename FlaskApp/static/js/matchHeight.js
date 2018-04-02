(function (a) {
    a.fn.matchHeight = function (b) {
        if ("remove" === b) {
            var f = this;
            this.css("height", "");
            a.each(a.fn.matchHeight._groups, function (g, h) {
                h.elements = h.elements.not(f)
            });
            return this
        }
        if (1 >= this.length) {
            return this
        }
        b = "undefined" !== typeof b ? b : !0;
        a.fn.matchHeight._groups.push({ elements: this, byRow: b });
        a.fn.matchHeight._apply(this, b);
        return this
    };
    a.fn.matchHeight._apply = function (b, g) {
        var h = a(b), f = [h];
        g && (h.css({ display: "block", "padding-top": "0", "padding-bottom": "0", "border-top": "0", "border-bottom": "0", height: "100px" }), f = c(h), h.css({ display: "", "padding-top": "", "padding-bottom": "", "border-top": "", "border-bottom": "", height: "" }));
        a.each(f, function (i, l) {
            var k = a(l), j = 0;
            k.each(function () {
                var m = a(this);
                m.css({ display: "block", height: "" });
                m.outerHeight(!1) > j && (j = m.outerHeight(!1));
                m.css({ display: "" })
            });
            k.each(function () {
                var m = a(this), n = 0; "border-box"
                !== m.css("box-sizing") && (n += e(m.css("border-top-width")) + e(m.css("border-bottom-width")), n += e(m.css("padding-top")) + e(m.css("padding-bottom")));
                m.css("height", j - n)
            })
        });
        return this
    };
    a.fn.matchHeight._applyDataApi = function () {
        var b = {};
        a("[data-match-height], [data-mh]").each(function () {
            var f = a(this), g = f.attr("data-match-height");
            b[g] = g in b ? b[g].add(f) : f
        });
        a.each(b, function () {
            this.matchHeight(!0)
        })
    };
    a.fn.matchHeight._groups = [];
    var d = -1;
    a.fn.matchHeight._update = function (b) {
        if (b && "resize" === b.type) {
            b = a(window).width();
            if (b === d) {
                return
            }
            d = b
        }
        a.each(a.fn.matchHeight._groups, function () {
            a.fn.matchHeight._apply(this.elements, this.byRow)
        })
    };
    a(a.fn.matchHeight._applyDataApi);
    a(window).bind("load resize orientationchange", a.fn.matchHeight._update);
    var c = function (b) {
        var f = null, g = [];
        a(b).each(function () {
            var i = a(this), k = i.offset().top - e(i.css("margin-top")), j = 0 < g.length ? g[g.length - 1] : null;
            null === j ? g.push(i) : 1 >= Math.floor(Math.abs(f - k)) ? g[g.length - 1] = j.add(i) : g.push(i);
            f = k
        });
        return g
    }, e = function (b) {
        return parseFloat(b) || 0
    }
})(jQuery);

$(document).ready(function () {
    $('.equal-height-panels .panel').matchHeight();
});
