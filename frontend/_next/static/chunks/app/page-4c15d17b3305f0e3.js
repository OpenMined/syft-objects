(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [931], {
    5758: function(e, s, t) {
      Promise.resolve().then(t.bind(t, 3031))
    },
    3031: function(e, s, t) {
      "use strict";
      t.r(s), t.d(s, {
        default: function() {
          return j
        }
      });
      var r = t(7437),
        a = t(2265),
        n = t(9915),
        c = t(9839),
        l = t(3835),
        i = t(7951),
        d = t(4457),
        o = t(7661),
        x = t(892),
        m = t(2374),
        u = t(9799);
      let h = (0, t(7865).Z)("Eye", [
        ["path", {
          d: "M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z",
          key: "rwhkz3"
        }],
        ["circle", {
          cx: "12",
          cy: "12",
          r: "3",
          key: "1v7zrd"
        }]
      ]);
      var p = t(6546),
        f = t(4213);

      function j() {
        let [e, s] = (0, a.useState)([]), [t, j] = (0, a.useState)(!0), [y, v] = (0, a.useState)(!1), [b, N] = (0, a.useState)(null), [g, w] = (0, a.useState)(null), [k, _] = (0, a.useState)(""), [Z, S] = (0, a.useState)(""), [C, E] = (0, a.useState)(null), [M, P] = (0, a.useState)(0), [R, L] = (0, a.useState)(null), [O, I] = (0, a.useState)("created_at"), [A, D] = (0, a.useState)("desc"), [F, T] = (0, a.useState)([]), [U, z] = (0, a.useState)(!0), [q, $] = (0, a.useState)(1), [B, W] = (0, a.useState)(25), [H, K] = (0, a.useState)(0), V = (0, a.useRef)(q), G = (0, a.useRef)(k), J = (0, a.useRef)(Z);
        (0, a.useEffect)(() => {
          V.current = q
        }, [q]), (0, a.useEffect)(() => {
          G.current = k
        }, [k]), (0, a.useEffect)(() => {
          J.current = Z
        }, [Z]);
        let Y = async () => {
          try {
            let e = await fetch("".concat("", "/api/status"));
            if (!e.ok) throw Error("Failed to fetch status");
            let s = await e.json();
            w(s)
          } catch (e) {
            console.error("Error fetching status:", e)
          }
        }, Q = async function(e, t) {
          let r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : q;
          try {
            let a = new URLSearchParams;
            e && a.append("search", e), t && a.append("email_filter", t), a.append("limit", B.toString()), a.append("offset", ((r - 1) * B).toString());
            let n = await fetch("".concat("", "/api/objects?").concat(a));
            if (!n.ok) throw Error("Failed to fetch objects: ".concat(n.statusText));
            let c = await n.json();
            s(c.objects), P(c.total_count), K(Math.ceil(c.total_count / B)), L(c.search_info || null), N(null)
          } catch (e) {
            N(e instanceof Error ? e.message : "Failed to fetch objects"), s([])
          }
        }, X = async () => {
          v(!0);
          try {
            if (!(await fetch("".concat("", "/api/objects/refresh"))).ok) throw Error("Failed to refresh objects");
            await Q(k, Z, q)
          } catch (e) {
            N(e instanceof Error ? e.message : "Failed to refresh objects")
          } finally {
            v(!1)
          }
        }, ee = () => {
          $(1), Q(k, Z, 1)
        }, es = e => {
          $(e), Q(k, Z, e)
        }, et = e => {
          W(e), $(1), setTimeout(() => {
            Q(k, Z, 1)
          }, 0)
        }, er = (0, a.useCallback)((e, s, t) => [...e].sort((e, r) => {
          let a = e[s],
            n = r[s];
          if (null == a && (a = ""), null == n && (n = ""), "created_at" === s || "updated_at" === s) {
            let e = a ? new Date(a).getTime() : 0,
              s = n ? new Date(n).getTime() : 0;
            return "desc" === t ? s - e : e - s
          }
          let c = String(a).toLowerCase(),
            l = String(n).toLowerCase();
          return c < l ? "desc" === t ? 1 : -1 : c > l ? "desc" === t ? -1 : 1 : 0
        }), []), ea = e => {
          let s = O === e && "desc" === A ? "asc" : "desc";
          I(e), D(s)
        };
        (0, a.useEffect)(() => {
          T(er(e, O, A))
        }, [e, O, A, er]);
        let en = e => {
            if (!e) return "N/A";
            try {
              return new Date(e).toLocaleString()
            } catch (e) {
              return "Invalid date"
            }
          },
          ec = e => {
            if (!e) return !1;
            try {
              let s = new Date(e).getTime();
              return (new Date().getTime() - s) / 1e3 < 10
            } catch (e) {
              return !1
            }
          };
        return ((0, a.useEffect)(() => {
          (async () => {
            j(!0), await Promise.all([Y(), Q()]), j(!1)
          })()
        }, []), (0, a.useEffect)(() => {
          if (!U) return;
          let e = setInterval(() => {
            Q(G.current, J.current, V.current)
          }, 1e3);
          return () => clearInterval(e)
        }, [U]), (0, a.useEffect)(() => {
          M > 0 && K(Math.ceil(M / B))
        }, [M, B]), t) ? (0, r.jsx)("div", {
          className: "flex items-center justify-center min-h-[400px]",
          children: (0, r.jsxs)("div", {
            className: "text-center space-y-4",
            children: [(0, r.jsx)(n.Z, {
              className: "h-8 w-8 animate-spin mx-auto text-blue-600"
            }), (0, r.jsx)("p", {
              className: "text-muted-foreground",
              children: "Loading syft objects..."
            })]
          })
        }) : (0, r.jsxs)("div", {
          className: "space-y-6",
          children: [g && (0, r.jsx)("div", {
            className: "bg-card rounded-lg border p-4",
            children: (0, r.jsxs)("div", {
              className: "flex items-center justify-between",
              children: [(0, r.jsxs)("div", {
                children: [(0, r.jsxs)("h2", {
                  className: "text-lg font-semibold",
                  children: [g.app, " v", g.version]
                }), (0, r.jsxs)("div", {
                  className: "flex items-center space-x-4 mt-2 text-sm text-muted-foreground",
                  children: [(0, r.jsxs)("span", {
                    className: "flex items-center space-x-1",
                    children: [(0, r.jsx)("div", {
                      className: "w-2 h-2 rounded-full ".concat("connected" === g.syftbox.status ? "bg-green-500" : "bg-red-500")
                    }), (0, r.jsxs)("span", {
                      children: ["SyftBox: ", g.syftbox.status]
                    })]
                  }), g.syftbox.user_email && (0, r.jsxs)("span", {
                    className: "flex items-center space-x-1",
                    children: [(0, r.jsx)(c.Z, {
                      className: "h-3 w-3"
                    }), (0, r.jsx)("span", {
                      children: g.syftbox.user_email
                    })]
                  }), (0, r.jsxs)("span", {
                    className: "flex items-center space-x-1",
                    children: [(0, r.jsx)("div", {
                      className: "w-2 h-2 rounded-full ".concat("available" === g.components.objects_collection ? "bg-green-500" : "bg-red-500")
                    }), (0, r.jsxs)("span", {
                      children: ["Objects: ", g.components.objects_collection]
                    })]
                  })]
                })]
              }), (0, r.jsxs)("div", {
                className: "flex space-x-2",
                children: [(0, r.jsxs)("button", {
                  onClick: () => z(!U),
                  className: "flex items-center space-x-2 px-4 py-2 rounded-lg ".concat(U ? "bg-green-100 text-green-800 hover:bg-green-200" : "bg-gray-100 text-gray-800 hover:bg-gray-200"),
                  children: [(0, r.jsx)("div", {
                    className: "w-2 h-2 rounded-full ".concat(U ? "bg-green-500" : "bg-gray-500")
                  }), (0, r.jsx)("span", {
                    children: "Auto"
                  })]
                }), (0, r.jsxs)("button", {
                  onClick: X,
                  disabled: y,
                  className: "flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50",
                  children: [(0, r.jsx)(n.Z, {
                    className: "h-4 w-4 ".concat(y ? "animate-spin" : "")
                  }), (0, r.jsx)("span", {
                    children: "Refresh"
                  })]
                })]
              })]
            })
          }), (0, r.jsxs)("div", {
            className: "bg-card rounded-lg border p-4",
            children: [(0, r.jsxs)("div", {
              className: "flex flex-col sm:flex-row gap-4",
              children: [(0, r.jsx)("div", {
                className: "flex-1",
                children: (0, r.jsxs)("div", {
                  className: "relative",
                  children: [(0, r.jsx)(l.Z, {
                    className: "absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground"
                  }), (0, r.jsx)("input", {
                    type: "text",
                    placeholder: "Search objects...",
                    value: k,
                    onChange: e => _(e.target.value),
                    onKeyPress: e => "Enter" === e.key && ee(),
                    className: "w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  })]
                })
              }), (0, r.jsx)("div", {
                className: "flex-1",
                children: (0, r.jsxs)("div", {
                  className: "relative",
                  children: [(0, r.jsx)(i.Z, {
                    className: "absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground"
                  }), (0, r.jsx)("input", {
                    type: "text",
                    placeholder: "Filter by email...",
                    value: Z,
                    onChange: e => S(e.target.value),
                    onKeyPress: e => "Enter" === e.key && ee(),
                    className: "w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  })]
                })
              }), (0, r.jsxs)("div", {
                className: "flex space-x-2",
                children: [(0, r.jsx)("button", {
                  onClick: ee,
                  className: "px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90",
                  children: "Search"
                }), (0, r.jsx)("button", {
                  onClick: () => {
                    _(""), S(""), $(1), Q("", "", 1)
                  },
                  className: "px-4 py-2 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/90",
                  children: "Clear"
                })]
              })]
            }), (0, r.jsxs)("div", {
              className: "mt-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-sm text-muted-foreground",
              children: [(0, r.jsxs)("div", {
                children: [R && "".concat(R, " • "), M, " objects total", O && (0, r.jsxs)("span", {
                  className: "ml-2",
                  children: ["• Sorted by ", "created_at" === O ? "creation date" : O, "(", "desc" === A ? "newest first" : "oldest first", ")"]
                }), (0, r.jsxs)("span", {
                  className: "ml-2",
                  children: ["• Showing ", (q - 1) * B + 1, "-", Math.min(q * B, M), " of ", M]
                })]
              }), (0, r.jsxs)("div", {
                className: "flex items-center space-x-4",
                children: [(0, r.jsxs)("div", {
                  className: "flex items-center space-x-2",
                  children: [(0, r.jsx)("span", {
                    className: "text-xs",
                    children: "Per page:"
                  }), (0, r.jsxs)("select", {
                    value: B,
                    onChange: e => et(Number(e.target.value)),
                    className: "text-xs border rounded px-2 py-1 bg-background",
                    children: [(0, r.jsx)("option", {
                      value: 10,
                      children: "10"
                    }), (0, r.jsx)("option", {
                      value: 25,
                      children: "25"
                    }), (0, r.jsx)("option", {
                      value: 50,
                      children: "50"
                    }), (0, r.jsx)("option", {
                      value: 100,
                      children: "100"
                    })]
                  })]
                }), (0, r.jsxs)("div", {
                  className: "flex items-center space-x-2",
                  children: [(0, r.jsx)("div", {
                    className: "w-2 h-2 rounded-full ".concat(U ? "bg-green-500 animate-pulse" : "bg-gray-400")
                  }), (0, r.jsx)("span", {
                    className: "text-xs",
                    children: U ? "Auto-refreshing every 1s" : "Auto-refresh disabled"
                  })]
                })]
              })]
            })]
          }), b && (0, r.jsx)("div", {
            className: "bg-destructive/10 border border-destructive/20 rounded-lg p-4",
            children: (0, r.jsxs)("p", {
              className: "text-destructive font-medium",
              children: ["Error: ", b]
            })
          }), (0, r.jsxs)("div", {
            className: "bg-card rounded-lg border overflow-hidden",
            children: [(0, r.jsx)("div", {
              className: "overflow-x-auto",
              children: (0, r.jsxs)("table", {
                className: "w-full",
                children: [(0, r.jsx)("thead", {
                  className: "bg-muted/50 border-b",
                  children: (0, r.jsxs)("tr", {
                    children: [(0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none",
                      onClick: () => ea("index"),
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)("span", {
                          children: "#"
                        }), "index" === O && ("desc" === A ? (0, r.jsx)(d.Z, {
                          className: "h-3 w-3"
                        }) : (0, r.jsx)(o.Z, {
                          className: "h-3 w-3"
                        }))]
                      })
                    }), (0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none",
                      onClick: () => ea("name"),
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)("span", {
                          children: "Name"
                        }), "name" === O && ("desc" === A ? (0, r.jsx)(d.Z, {
                          className: "h-3 w-3"
                        }) : (0, r.jsx)(o.Z, {
                          className: "h-3 w-3"
                        }))]
                      })
                    }), (0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none",
                      onClick: () => ea("email"),
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)("span", {
                          children: "Email"
                        }), "email" === O && ("desc" === A ? (0, r.jsx)(d.Z, {
                          className: "h-3 w-3"
                        }) : (0, r.jsx)(o.Z, {
                          className: "h-3 w-3"
                        }))]
                      })
                    }), (0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium",
                      children: "Files"
                    }), (0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium cursor-pointer hover:bg-muted/75 select-none",
                      onClick: () => ea("created_at"),
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)("span", {
                          children: "Created"
                        }), "created_at" === O && ("desc" === A ? (0, r.jsx)(d.Z, {
                          className: "h-3 w-3"
                        }) : (0, r.jsx)(o.Z, {
                          className: "h-3 w-3"
                        }))]
                      })
                    }), (0, r.jsx)("th", {
                      className: "text-left px-4 py-3 font-medium",
                      children: "Actions"
                    })]
                  })
                }), (0, r.jsx)("tbody", {
                  children: 0 === F.length ? (0, r.jsx)("tr", {
                    children: (0, r.jsx)("td", {
                      colSpan: 6,
                      className: "px-4 py-8 text-center text-muted-foreground",
                      children: t ? "Loading..." : "No syft objects found"
                    })
                  }) : F.map(e => (0, r.jsxs)("tr", {
                    className: "border-b transition-colors hover:bg-muted/50 ".concat(ec(e.created_at) ? "rainbow-bg" : ""),
                    children: [(0, r.jsx)("td", {
                      className: "px-4 py-3 text-sm",
                      children: e.index
                    }), (0, r.jsx)("td", {
                      className: "px-4 py-3",
                      children: (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("div", {
                          className: "font-medium",
                          children: e.name
                        }), e.description && (0, r.jsx)("div", {
                          className: "text-sm text-muted-foreground truncate max-w-xs",
                          children: e.description
                        })]
                      })
                    }), (0, r.jsx)("td", {
                      className: "px-4 py-3 text-sm",
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)(c.Z, {
                          className: "h-3 w-3 text-muted-foreground"
                        }), (0, r.jsx)("span", {
                          children: e.email
                        })]
                      })
                    }), (0, r.jsx)("td", {
                      className: "px-4 py-3",
                      children: (0, r.jsxs)("div", {
                        className: "flex space-x-2",
                        children: [(0, r.jsxs)("div", {
                          className: "flex items-center space-x-1 px-2 py-1 rounded text-xs ".concat(e.file_exists.private ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"),
                          children: [(0, r.jsx)(x.Z, {
                            className: "h-3 w-3"
                          }), (0, r.jsx)("span", {
                            children: "Private"
                          })]
                        }), (0, r.jsxs)("div", {
                          className: "flex items-center space-x-1 px-2 py-1 rounded text-xs ".concat(e.file_exists.mock ? "bg-blue-100 text-blue-800" : "bg-gray-100 text-gray-800"),
                          children: [(0, r.jsx)(m.Z, {
                            className: "h-3 w-3"
                          }), (0, r.jsx)("span", {
                            children: "Mock"
                          })]
                        })]
                      })
                    }), (0, r.jsx)("td", {
                      className: "px-4 py-3 text-sm text-muted-foreground",
                      children: (0, r.jsxs)("div", {
                        className: "flex items-center space-x-1",
                        children: [(0, r.jsx)(u.Z, {
                          className: "h-3 w-3"
                        }), (0, r.jsx)("span", {
                          children: en(e.created_at)
                        })]
                      })
                    }), (0, r.jsx)("td", {
                      className: "px-4 py-3",
                      children: (0, r.jsxs)("button", {
                        onClick: () => E(e),
                        className: "flex items-center space-x-1 px-3 py-1 bg-primary text-primary-foreground rounded text-sm hover:bg-primary/90",
                        children: [(0, r.jsx)(h, {
                          className: "h-3 w-3"
                        }), (0, r.jsx)("span", {
                          children: "View"
                        })]
                      })
                    })]
                  }, e.uid))
                })]
              })
            }), H > 1 && (0, r.jsxs)("div", {
              className: "flex items-center justify-between px-4 py-3 border-t",
              children: [(0, r.jsxs)("div", {
                className: "text-sm text-muted-foreground",
                children: ["Page ", q, " of ", H]
              }), (0, r.jsxs)("div", {
                className: "flex items-center space-x-2",
                children: [(0, r.jsxs)("button", {
                  onClick: () => es(q - 1),
                  disabled: q <= 1,
                  className: "flex items-center space-x-1 px-3 py-1 border rounded-lg hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed",
                  children: [(0, r.jsx)(p.Z, {
                    className: "h-4 w-4"
                  }), (0, r.jsx)("span", {
                    children: "Previous"
                  })]
                }), (0, r.jsx)("div", {
                  className: "flex items-center space-x-1",
                  children: Array.from({
                    length: Math.min(5, H)
                  }, (e, s) => {
                    let t;
                    return t = H <= 5 ? s + 1 : q <= 3 ? s + 1 : q >= H - 2 ? H - 4 + s : q - 2 + s, (0, r.jsx)("button", {
                      onClick: () => es(t),
                      className: "px-3 py-1 text-sm rounded ".concat(q === t ? "bg-primary text-primary-foreground" : "hover:bg-muted"),
                      children: t
                    }, t)
                  })
                }), (0, r.jsxs)("button", {
                  onClick: () => es(q + 1),
                  disabled: q >= H,
                  className: "flex items-center space-x-1 px-3 py-1 border rounded-lg hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed",
                  children: [(0, r.jsx)("span", {
                    children: "Next"
                  }), (0, r.jsx)(f.Z, {
                    className: "h-4 w-4"
                  })]
                })]
              })]
            })]
          }), C && (0, r.jsx)("div", {
            className: "fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50",
            children: (0, r.jsxs)("div", {
              className: "bg-background rounded-lg max-w-6xl max-h-[90vh] overflow-y-auto w-full",
              children: [(0, r.jsx)("div", {
                className: "sticky top-0 bg-background border-b px-6 py-4",
                children: (0, r.jsxs)("div", {
                  className: "flex items-center justify-between",
                  children: [(0, r.jsx)("h2", {
                    className: "text-xl font-semibold",
                    children: C.name
                  }), (0, r.jsx)("button", {
                    onClick: () => E(null),
                    className: "text-muted-foreground hover:text-foreground",
                    children: "✕"
                  })]
                })
              }), (0, r.jsxs)("div", {
                className: "p-6 space-y-6",
                children: [(0, r.jsxs)("div", {
                  className: "grid md:grid-cols-2 gap-4",
                  children: [(0, r.jsxs)("div", {
                    children: [(0, r.jsx)("h3", {
                      className: "font-medium mb-2",
                      children: "Basic Information"
                    }), (0, r.jsxs)("div", {
                      className: "space-y-2 text-sm",
                      children: [(0, r.jsxs)("div", {
                        children: [(0, r.jsx)("div", {
                          className: "font-medium mb-1",
                          children: "UID:"
                        }), (0, r.jsx)("code", {
                          className: "text-xs bg-muted px-2 py-1 rounded block break-all",
                          children: C.uid
                        })]
                      }), (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("span", {
                          className: "font-medium",
                          children: "Email:"
                        }), " ", C.email]
                      }), (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("span", {
                          className: "font-medium",
                          children: "Created:"
                        }), " ", en(C.created_at)]
                      }), (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("span", {
                          className: "font-medium",
                          children: "Updated:"
                        }), " ", en(C.updated_at)]
                      })]
                    })]
                  }), (0, r.jsxs)("div", {
                    children: [(0, r.jsx)("h3", {
                      className: "font-medium mb-2",
                      children: "URLs"
                    }), (0, r.jsxs)("div", {
                      className: "space-y-3 text-sm",
                      children: [(0, r.jsxs)("div", {
                        children: [(0, r.jsx)("div", {
                          className: "font-medium mb-1",
                          children: "Private:"
                        }), (0, r.jsx)("code", {
                          className: "text-xs bg-muted px-2 py-1 rounded block break-all",
                          children: C.private_url
                        })]
                      }), (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("div", {
                          className: "font-medium mb-1",
                          children: "Mock:"
                        }), (0, r.jsx)("code", {
                          className: "text-xs bg-muted px-2 py-1 rounded block break-all",
                          children: C.mock_url
                        })]
                      }), (0, r.jsxs)("div", {
                        children: [(0, r.jsx)("div", {
                          className: "font-medium mb-1",
                          children: "Metadata:"
                        }), (0, r.jsx)("code", {
                          className: "text-xs bg-muted px-2 py-1 rounded block break-all",
                          children: C.syftobject_url
                        })]
                      })]
                    })]
                  })]
                }), C.description && (0, r.jsxs)("div", {
                  children: [(0, r.jsx)("h3", {
                    className: "font-medium mb-2",
                    children: "Description"
                  }), (0, r.jsx)("p", {
                    className: "text-sm text-muted-foreground",
                    children: C.description
                  })]
                }), (0, r.jsxs)("div", {
                  children: [(0, r.jsx)("h3", {
                    className: "font-medium mb-2",
                    children: "Permissions"
                  }), (0, r.jsxs)("div", {
                    className: "grid md:grid-cols-2 gap-4 text-sm",
                    children: [(0, r.jsxs)("div", {
                      children: [(0, r.jsx)("div", {
                        className: "font-medium text-xs text-muted-foreground mb-1",
                        children: "READ PERMISSIONS"
                      }), (0, r.jsxs)("div", {
                        className: "space-y-1",
                        children: [(0, r.jsxs)("div", {
                          children: [(0, r.jsx)("span", {
                            className: "font-medium",
                            children: "Metadata:"
                          }), " ", C.permissions.syftobject.join(", ") || "None"]
                        }), (0, r.jsxs)("div", {
                          children: [(0, r.jsx)("span", {
                            className: "font-medium",
                            children: "Mock:"
                          }), " ", C.permissions.mock_read.join(", ") || "None"]
                        }), (0, r.jsxs)("div", {
                          children: [(0, r.jsx)("span", {
                            className: "font-medium",
                            children: "Private:"
                          }), " ", C.permissions.private_read.join(", ") || "None"]
                        })]
                      })]
                    }), (0, r.jsxs)("div", {
                      children: [(0, r.jsx)("div", {
                        className: "font-medium text-xs text-muted-foreground mb-1",
                        children: "WRITE PERMISSIONS"
                      }), (0, r.jsxs)("div", {
                        className: "space-y-1",
                        children: [(0, r.jsxs)("div", {
                          children: [(0, r.jsx)("span", {
                            className: "font-medium",
                            children: "Mock:"
                          }), " ", C.permissions.mock_write.join(", ") || "None"]
                        }), (0, r.jsxs)("div", {
                          children: [(0, r.jsx)("span", {
                            className: "font-medium",
                            children: "Private:"
                          }), " ", C.permissions.private_write.join(", ") || "None"]
                        })]
                      })]
                    })]
                  })]
                }), Object.keys(C.metadata).length > 0 && (0, r.jsxs)("div", {
                  children: [(0, r.jsx)("h3", {
                    className: "font-medium mb-2",
                    children: "Metadata"
                  }), (0, r.jsx)("div", {
                    className: "bg-muted rounded p-3",
                    children: (0, r.jsx)("pre", {
                      className: "text-xs overflow-auto",
                      children: JSON.stringify(C.metadata, null, 2)
                    })
                  })]
                })]
              })]
            })
          })]
        })
      }
    },
    622: function(e, s, t) {
      "use strict";
      var r = t(2265),
        a = Symbol.for("react.element"),
        n = Symbol.for("react.fragment"),
        c = Object.prototype.hasOwnProperty,
        l = r.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
        i = {
          key: !0,
          ref: !0,
          __self: !0,
          __source: !0
        };

      function d(e, s, t) {
        var r, n = {},
          d = null,
          o = null;
        for (r in void 0 !== t && (d = "" + t), void 0 !== s.key && (d = "" + s.key), void 0 !== s.ref && (o = s.ref), s) c.call(s, r) && !i.hasOwnProperty(r) && (n[r] = s[r]);
        if (e && e.defaultProps)
          for (r in s = e.defaultProps) void 0 === n[r] && (n[r] = s[r]);
        return {
          $$typeof: a,
          type: e,
          key: d,
          ref: o,
          props: n,
          _owner: l.current
        }
      }
      s.Fragment = n, s.jsx = d, s.jsxs = d
    },
    7437: function(e, s, t) {
      "use strict";
      e.exports = t(622)
    },
    7865: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return c
        }
      });
      var r = t(2265),
        a = {
          xmlns: "http://www.w3.org/2000/svg",
          width: 24,
          height: 24,
          viewBox: "0 0 24 24",
          fill: "none",
          stroke: "currentColor",
          strokeWidth: 2,
          strokeLinecap: "round",
          strokeLinejoin: "round"
        };
      let n = e => e.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
      var c = (e, s) => {
        let t = (0, r.forwardRef)(({
          color: t = "currentColor",
          size: c = 24,
          strokeWidth: l = 2,
          absoluteStrokeWidth: i,
          children: d,
          ...o
        }, x) => (0, r.createElement)("svg", {
          ref: x,
          ...a,
          width: c,
          height: c,
          stroke: t,
          strokeWidth: i ? 24 * Number(l) / Number(c) : l,
          className: `lucide lucide-${n(e)}`,
          ...o
        }, [...s.map(([e, s]) => (0, r.createElement)(e, s)), ...(Array.isArray(d) ? d : [d]) || []]));
        return t.displayName = `${e}`, t
      }
    },
    9799: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("Calendar", [
        ["rect", {
          width: "18",
          height: "18",
          x: "3",
          y: "4",
          rx: "2",
          ry: "2",
          key: "eu3xkr"
        }],
        ["line", {
          x1: "16",
          x2: "16",
          y1: "2",
          y2: "6",
          key: "m3sa8f"
        }],
        ["line", {
          x1: "8",
          x2: "8",
          y1: "2",
          y2: "6",
          key: "18kwsl"
        }],
        ["line", {
          x1: "3",
          x2: "21",
          y1: "10",
          y2: "10",
          key: "xt86sb"
        }]
      ])
    },
    4457: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("ChevronDown", [
        ["path", {
          d: "m6 9 6 6 6-6",
          key: "qrunsl"
        }]
      ])
    },
    6546: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("ChevronLeft", [
        ["path", {
          d: "m15 18-6-6 6-6",
          key: "1wnfg3"
        }]
      ])
    },
    4213: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("ChevronRight", [
        ["path", {
          d: "m9 18 6-6-6-6",
          key: "mthhwq"
        }]
      ])
    },
    7661: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("ChevronUp", [
        ["path", {
          d: "m18 15-6-6-6 6",
          key: "153udz"
        }]
      ])
    },
    7951: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("Filter", [
        ["polygon", {
          points: "22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3",
          key: "1yg77f"
        }]
      ])
    },
    2374: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("Globe", [
        ["circle", {
          cx: "12",
          cy: "12",
          r: "10",
          key: "1mglay"
        }],
        ["line", {
          x1: "2",
          x2: "22",
          y1: "12",
          y2: "12",
          key: "1dnqot"
        }],
        ["path", {
          d: "M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z",
          key: "nb9nel"
        }]
      ])
    },
    892: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("Lock", [
        ["rect", {
          width: "18",
          height: "11",
          x: "3",
          y: "11",
          rx: "2",
          ry: "2",
          key: "1w4ew1"
        }],
        ["path", {
          d: "M7 11V7a5 5 0 0 1 10 0v4",
          key: "fwvmzm"
        }]
      ])
    },
    9915: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("RefreshCw", [
        ["path", {
          d: "M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8",
          key: "v9h5vc"
        }],
        ["path", {
          d: "M21 3v5h-5",
          key: "1q7to0"
        }],
        ["path", {
          d: "M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16",
          key: "3uifl3"
        }],
        ["path", {
          d: "M8 16H3v5",
          key: "1cv678"
        }]
      ])
    },
    3835: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("Search", [
        ["circle", {
          cx: "11",
          cy: "11",
          r: "8",
          key: "4ej97u"
        }],
        ["path", {
          d: "m21 21-4.3-4.3",
          key: "1qie3q"
        }]
      ])
    },
    9839: function(e, s, t) {
      "use strict";
      t.d(s, {
        Z: function() {
          return r
        }
      });
      let r = (0, t(7865).Z)("User", [
        ["path", {
          d: "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2",
          key: "975kel"
        }],
        ["circle", {
          cx: "12",
          cy: "7",
          r: "4",
          key: "17ys0d"
        }]
      ])
    }
  },
  function(e) {
    e.O(0, [971, 938, 744], function() {
      return e(e.s = 5758)
    }), _N_E = e.O()
  }
]);