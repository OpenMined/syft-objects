"use strict";
(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
  [350], {
    4350: function(e, t, s) {
      s.r(t), s.d(t, {
        default: function() {
          return g
        }
      });
      var a = s(7437),
        l = s(2265),
        n = s(3835),
        i = s(7951),
        r = s(4457),
        o = s(7661),
        c = s(9839),
        d = s(9799),
        x = s(2374),
        m = s(892);
      let u = (0, s(7865).Z)("Trash2", [
        ["path", {
          d: "M3 6h18",
          key: "d0wm0j"
        }],
        ["path", {
          d: "M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6",
          key: "4alrt4"
        }],
        ["path", {
          d: "M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2",
          key: "v07s0e"
        }],
        ["line", {
          x1: "10",
          x2: "10",
          y1: "11",
          y2: "17",
          key: "1uufr5"
        }],
        ["line", {
          x1: "14",
          x2: "14",
          y1: "11",
          y2: "17",
          key: "xtxkd"
        }]
      ]);
      var p = s(6546),
        h = s(4213),
        f = s(9915);

      function j(e) {
        let {
          className: t = "h-8 w-8",
          isLoading: s = !1
        } = e, [n, i] = (0, l.useState)(!1), [r, o] = (0, l.useState)(!1);
        return ((0, l.useEffect)(() => {
          if (!s && !n) {
            let e = setTimeout(() => i(!0), 500),
              t = setTimeout(() => i(!1), 2e3);
            return () => {
              clearTimeout(e), clearTimeout(t)
            }
          }
        }, [s, n]), (0, l.useEffect)(() => {
          if (s) {
            let e = setInterval(() => {
              o(!0), setTimeout(() => o(!1), 400)
            }, 1600);
            return () => clearInterval(e)
          }
        }, [s]), n) ? (0, a.jsx)("div", {
          className: "".concat(t, " text-4xl animate-bounce"),
          children: "\uD83E\uDD99"
        }) : (0, a.jsxs)("svg", {
          className: "".concat(t, " ").concat(s ? "syftbox-loading" : "", " ").concat(r ? "syftbox-explosion" : ""),
          viewBox: "0 0 311 360",
          fill: "none",
          xmlns: "http://www.w3.org/2000/svg",
          children: [(0, a.jsxs)("g", {
            clipPath: "url(#clip0_7523_4240)",
            children: [(0, a.jsx)("path", {
              d: "M311.414 89.7878L155.518 179.998L-0.378906 89.7878L155.518 -0.422485L311.414 89.7878Z",
              fill: "url(#paint0_linear_7523_4240)"
            }), (0, a.jsx)("path", {
              d: "M311.414 89.7878V270.208L155.518 360.423V179.998L311.414 89.7878Z",
              fill: "url(#paint1_linear_7523_4240)"
            }), (0, a.jsx)("path", {
              d: "M155.518 179.998V360.423L-0.378906 270.208V89.7878L155.518 179.998Z",
              fill: "url(#paint2_linear_7523_4240)"
            })]
          }), (0, a.jsxs)("defs", {
            children: [(0, a.jsxs)("linearGradient", {
              id: "paint0_linear_7523_4240",
              x1: "-0.378904",
              y1: "89.7878",
              x2: "311.414",
              y2: "89.7878",
              gradientUnits: "userSpaceOnUse",
              children: [(0, a.jsx)("stop", {
                stopColor: "#DC7A6E"
              }), (0, a.jsx)("stop", {
                offset: "0.251496",
                stopColor: "#F6A464"
              }), (0, a.jsx)("stop", {
                offset: "0.501247",
                stopColor: "#FDC577"
              }), (0, a.jsx)("stop", {
                offset: "0.753655",
                stopColor: "#EFC381"
              }), (0, a.jsx)("stop", {
                offset: "1",
                stopColor: "#B9D599"
              })]
            }), (0, a.jsxs)("linearGradient", {
              id: "paint1_linear_7523_4240",
              x1: "309.51",
              y1: "89.7878",
              x2: "155.275",
              y2: "360.285",
              gradientUnits: "userSpaceOnUse",
              children: [(0, a.jsx)("stop", {
                stopColor: "#BFCD94"
              }), (0, a.jsx)("stop", {
                offset: "0.245025",
                stopColor: "#B2D69E"
              }), (0, a.jsx)("stop", {
                offset: "0.504453",
                stopColor: "#8DCCA6"
              }), (0, a.jsx)("stop", {
                offset: "0.745734",
                stopColor: "#5CB8B7"
              }), (0, a.jsx)("stop", {
                offset: "1",
                stopColor: "#4CA5B8"
              })]
            }), (0, a.jsxs)("linearGradient", {
              id: "paint2_linear_7523_4240",
              x1: "-0.378906",
              y1: "89.7878",
              x2: "155.761",
              y2: "360.282",
              gradientUnits: "userSpaceOnUse",
              children: [(0, a.jsx)("stop", {
                stopColor: "#D7686D"
              }), (0, a.jsx)("stop", {
                offset: "0.225",
                stopColor: "#C64B77"
              }), (0, a.jsx)("stop", {
                offset: "0.485",
                stopColor: "#A2638E"
              }), (0, a.jsx)("stop", {
                offset: "0.703194",
                stopColor: "#758AA8"
              }), (0, a.jsx)("stop", {
                offset: "1",
                stopColor: "#639EAF"
              })]
            }), (0, a.jsx)("clipPath", {
              id: "clip0_7523_4240",
              children: (0, a.jsx)("rect", {
                width: "311",
                height: "360",
                fill: "white"
              })
            })]
          })]
        })
      }

      function b(e) {
        let {
          permissions: t,
          onAddPermission: s,
          onRemovePermission: n
        } = e, [i, r] = (0, l.useState)({
          private_read: "",
          private_write: "",
          mock_read: "",
          mock_write: "",
          syftobject: ""
        }), o = e => {
          let t = i[e];
          t.trim() && (s(e, t.trim()), r(t => ({
            ...t,
            [e]: ""
          })))
        };
        return (0, a.jsx)("div", {
          className: "space-y-4",
          children: [{
            key: "private_read",
            label: "Private Read",
            color: "text-green-700"
          }, {
            key: "private_write",
            label: "Private Write",
            color: "text-green-800"
          }, {
            key: "mock_read",
            label: "Mock Read",
            color: "text-blue-700"
          }, {
            key: "mock_write",
            label: "Mock Write",
            color: "text-blue-800"
          }, {
            key: "syftobject",
            label: "Syft Object",
            color: "text-purple-700"
          }].map(e => {
            let {
              key: s,
              label: l,
              color: c
            } = e;
            return (0, a.jsxs)("div", {
              className: "border rounded p-3",
              children: [(0, a.jsx)("h4", {
                className: "font-medium ".concat(c, " mb-2"),
                children: l
              }), (0, a.jsxs)("div", {
                className: "space-y-2",
                children: [(0, a.jsx)("div", {
                  className: "flex flex-wrap gap-1",
                  children: t[s].map(e => (0, a.jsxs)("span", {
                    className: "flex items-center bg-gray-100 text-gray-800 px-2 py-1 rounded text-xs",
                    children: [e, (0, a.jsx)("button", {
                      onClick: () => n(s, e),
                      className: "ml-1 text-red-500 hover:text-red-700",
                      children: "\xd7"
                    })]
                  }, e))
                }), (0, a.jsxs)("div", {
                  className: "flex space-x-2",
                  children: [(0, a.jsx)("input", {
                    type: "text",
                    placeholder: "Add email or 'public'",
                    value: i[s],
                    onChange: e => r(t => ({
                      ...t,
                      [s]: e.target.value
                    })),
                    onKeyPress: e => "Enter" === e.key && o(s),
                    className: "flex-1 px-2 py-1 border rounded text-xs"
                  }), (0, a.jsx)("button", {
                    onClick: () => o(s),
                    className: "px-2 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600",
                    children: "Add"
                  })]
                })]
              })]
            }, s)
          })
        })
      }

      function g() {
        let [e, t] = (0, l.useState)([]), [s, g] = (0, l.useState)(!0), [y, v] = (0, l.useState)(!1), [N, w] = (0, l.useState)(null), [k, C] = (0, l.useState)(null), [_, D] = (0, l.useState)(""), [S, E] = (0, l.useState)(""), [Z, T] = (0, l.useState)(null), [O, P] = (0, l.useState)(0), [L, A] = (0, l.useState)(null), [F, U] = (0, l.useState)("created_at"), [M, R] = (0, l.useState)("desc"), [I, B] = (0, l.useState)([]), [W, z] = (0, l.useState)(!0), [V, q] = (0, l.useState)(new Set), [$, J] = (0, l.useState)(!1), [G, H] = (0, l.useState)(""), [K, Y] = (0, l.useState)(""), [Q, X] = (0, l.useState)(1), [ee, et] = (0, l.useState)(50), [es, ea] = (0, l.useState)(0), [el, en] = (0, l.useState)({
          isOpen: !1,
          title: "",
          content: "",
          editedContent: "",
          loading: !1,
          saving: !1,
          fileType: null,
          objectUid: null,
          canWrite: !1
        }), [ei, er] = (0, l.useState)({
          isOpen: !1,
          object: null,
          loading: !1
        }), [eo, ec] = (0, l.useState)(!1), [ed, ex] = (0, l.useState)(null), [em, eu] = (0, l.useState)(!1), [ep, eh] = (0, l.useState)(null), [ef, ej] = (0, l.useState)(null), [eb, eg] = (0, l.useState)(new Set), [ey, ev] = (0, l.useState)(null), eN = e => {
          ev("copied to clipboard: ".concat(e)), setTimeout(() => ev(null), 3e3)
        }, ew = async () => {
          try {
            let e = await fetch("".concat("", "/api/status"));
            if (!e.ok) throw Error("Failed to fetch status");
            let t = await e.json();
            C(t)
          } catch (e) {
            console.error("Error fetching status:", e)
          }
        }, ek = async () => {
          try {
            let e = await fetch("".concat("", "/api/objects"));
            if (!e.ok) throw Error("Failed to fetch objects: ".concat(e.statusText));
            let s = await e.json();
            t(s.objects), w(null)
          } catch (e) {
            w(e instanceof Error ? e.message : "Failed to fetch objects"), t([])
          }
        }, eC = () => {
          X(1)
        },         e_ = (e, t) => {
          if (!t) return !0;
          let s = t.toLowerCase(),
            a = [e.name, e.description, e.type, e.email, e.uid, e.private_url, e.mock_url, e.syftobject_url, e.index.toString()];
          return [...a, ...[e.created_at, e.updated_at].filter(Boolean).map(e => {
            if (!e) return "";
            try {
              return new Date(e).toLocaleString().toLowerCase()
            } catch (t) {
              return e.toLowerCase()
            }
          }), ...e.permissions.syftobject, ...e.permissions.mock_read, ...e.permissions.mock_write, ...e.permissions.private_read, ...e.permissions.private_write, JSON.stringify(e.metadata).toLowerCase()].some(e => e && e.toString().toLowerCase().includes(s))
        }, eD = () => {
          let e = I.slice((Q - 1) * ee, Q * ee).map(e => e.uid);
          if (e.every(e => V.has(e))) {
            let t = new Set(V);
            e.forEach(e => t.delete(e)), q(t)
          } else {
            let t = new Set(V);
            e.forEach(e => t.add(e)), q(t)
          }
        }, eS = e => {
          let t = new Set(V);
          t.has(e) ? t.delete(e) : t.add(e), q(t)
        };
        (0, l.useEffect)(() => {
          let e = I.slice((Q - 1) * ee, Q * ee).map(e => e.uid);
          J(e.length > 0 && e.every(e => V.has(e)))
        }, [V, I, Q, ee]);
        let eE = e => {
            X(e)
          },
          eZ = (0, l.useCallback)((e, t, s) => [...e].sort((e, a) => {
            let l = e[t],
              n = a[t];
            if (null == l && (l = ""), null == n && (n = ""), "index" === t) {
              let e = Number(l),
                t = Number(n);
              return "desc" === s ? t - e : e - t
            }
            if ("created_at" === t || "updated_at" === t) {
              let e = l ? new Date(l).getTime() : 0,
                t = n ? new Date(n).getTime() : 0;
              return "desc" === s ? t - e : e - t
            }
            let i = String(l).toLowerCase(),
              r = String(n).toLowerCase();
            return i < r ? "desc" === s ? 1 : -1 : i > r ? "desc" === s ? -1 : 1 : 0
          }), []),
          eT = e => {
            let t = F === e && "desc" === M ? "asc" : "desc";
            U(e), R(t)
          },
          eO = e => e.startsWith("syft://") ? "".concat("", "/api/file?syft_url=").concat(encodeURIComponent(e)) : e,
          eP = async function(e, t, s, a) {
            let l = arguments.length > 4 && void 0 !== arguments[4] && arguments[4];
            en({
              isOpen: !0,
              title: t,
              content: "",
              editedContent: "",
              loading: !0,
              saving: !1,
              fileType: s,
              objectUid: a,
              canWrite: l
            });
            try {
              let t = eO(e),
                s = await fetch(t);
              if (!s.ok) throw Error("Failed to fetch file: ".concat(s.statusText));
              let a = await s.text();
              en(e => ({
                ...e,
                content: a,
                editedContent: a,
                loading: !1
              }))
            } catch (t) {
              let e = "Error loading file: ".concat(t instanceof Error ? t.message : "Unknown error");
              en(t => ({
                ...t,
                content: e,
                editedContent: e,
                loading: !1
              }))
            }
          }, eL = async () => {
            if (el.fileType && el.objectUid) {
              en(e => ({
                ...e,
                saving: !0
              }));
              try {
                let e = await fetch("".concat("", "/api/objects/").concat(el.objectUid, "/file/").concat(el.fileType), {
                  method: "PUT",
                  headers: {
                    "Content-Type": "text/plain"
                  },
                  body: el.editedContent
                });
                if (!e.ok) throw Error("Failed to save file: ".concat(e.statusText));
                en(e => ({
                  ...e,
                  content: e.editedContent,
                  saving: !1
                })), await ek()
              } catch (e) {
                w(e instanceof Error ? e.message : "Failed to save file"), en(e => ({
                  ...e,
                  saving: !1
                }))
              }
            }
          }, eA = async e => {
            try {
              if (console.log("\uD83D\uDE80 Starting copy operation..."), console.log("\uD83D\uDD0D Clipboard API available:", !!navigator.clipboard), console.log("\uD83D\uDD0D WriteText available:", !!(navigator.clipboard && navigator.clipboard.writeText)), console.log("\uD83D\uDD0D Is secure context:", window.isSecureContext), console.log("\uD83D\uDD0D Document has focus:", document.hasFocus()), navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
                console.log("\uD83D\uDCCB Attempting modern clipboard API...");
                try {
                  let e = await navigator.permissions.query({
                    name: "clipboard-write"
                  });
                  console.log("\uD83D\uDD0D Clipboard permission:", e.state)
                } catch (e) {
                  console.log("\uD83D\uDD0D Could not check clipboard permissions:", e)
                }
                await navigator.clipboard.writeText(e), console.log("✅ Copied to clipboard (modern API):", e.substring(0, 20) + "..."), eN(e);
                return
              }
              console.log("\uD83D\uDCCB Using fallback clipboard method...");
              let t = document.createElement("textarea");
              t.value = e, t.style.position = "fixed", t.style.left = "-999999px", t.style.top = "-999999px", t.style.width = "1px", t.style.height = "1px", t.style.opacity = "0", document.body.appendChild(t);
              try {
                t.focus(), t.select(), t.setSelectionRange(0, e.length);
                let s = document.execCommand("copy");
                if (console.log("\uD83D\uDD0D execCommand copy result:", s), s) console.log("✅ Copied to clipboard (fallback):", e.substring(0, 20) + "..."), eN(e);
                else throw Error("execCommand copy failed")
              } finally {
                document.body.removeChild(t)
              }
            } catch (t) {
              console.error("❌ Copy operation failed:", t), console.error("❌ Error details:", {
                name: t.name,
                message: t.message,
                stack: t.stack
              });
              try {
                console.log("\uD83D\uDCCB Trying final fallback method...");
                let t = document.createElement("input");
                t.value = e, t.style.position = "fixed", t.style.left = "-999999px", t.style.top = "-999999px", document.body.appendChild(t), t.focus(), t.select();
                let s = document.execCommand("copy");
                if (document.body.removeChild(t), s) console.log("✅ Copied to clipboard (final fallback)!"), eN(e);
                else throw Error("All copy methods failed")
              } catch (e) {
                console.error("❌ Final fallback also failed:", e), eN("Failed to copy to clipboard")
              }
            }
          },         eF = async e => {
            let t = "";
            try {
            // Try to get the actual file path from the API
            let s = await fetch("".concat("", "/api/objects/").concat(e.uid));
            if (s.ok) {
              let a = await s.json();
              if (a.file_paths && a.file_paths.syftobject) {
                t = a.file_paths.syftobject;
              } else if (a.file_paths && a.file_paths.private) {
                t = a.file_paths.private;
              } else if (a.file_paths && a.file_paths.mock) {
                t = a.file_paths.mock;
              }
            }
            
            // Fallback to constructing from URL if API doesn't have file_paths
            if (!t && e.syftobject_url) {
              let s = e.syftobject_url.replace("syft://", ""),
                a = s.split("/")[0], // This gets "andrew@openmined.org"
                l = "/" + s.split("/").slice(1).join("/");
              t = "~/SyftBox/datasites/".concat(a).concat(l)
            }
            if (!t && e.private_url) {
              let s = e.private_url.replace("syft://", ""),
                a = s.split("/")[0], // This gets "andrew@openmined.org"
                l = "/" + s.split("/").slice(1).join("/");
                t = "~/SyftBox/datasites/".concat(a).concat(l)
              }
              if (!t && e.mock_url) {
              let s = e.mock_url.replace("syft://", ""),
                a = s.split("/")[0], // This gets "andrew@openmined.org"
                l = "/" + s.split("/").slice(1).join("/");
                t = "~/SyftBox/datasites/".concat(a).concat(l)
              }
              if (t) await eA(t);
              else throw Error("Could not determine local path")
            } catch (t) {
            await eA(e.syftobject_url || e.private_url || e.mock_url || "Path not available")
            }
          }, eU = e => {
            if (Z && Z.uid === e) return Z.permissions;
            let t = I.find(t => t.uid === e);
            return (null == t ? void 0 : t.permissions) || null
          }, eM = async () => {
            if (Z && ed) {
              eu(!0);
              try {
                console.log("\uD83D\uDD27 Saving permissions for object:", Z.uid), console.log("\uD83D\uDD27 Permissions payload:", ed);
                let e = await fetch("".concat("", "/api/objects/").concat(Z.uid, "/permissions"), {
                    method: "PUT",
                    headers: {
                      "Content-Type": "application/json"
                    },
                    body: JSON.stringify(ed)
                  }),
                  t = await e.text();
                if (console.log("\uD83D\uDD27 Response status:", e.status), console.log("\uD83D\uDD27 Response data:", t), !e.ok) throw Error("Failed to save permissions: ".concat(e.status, " ").concat(e.statusText, " - ").concat(t));
                let s = {
                  ...Z,
                  permissions: ed
                };
                T(s), await ek(), ec(!1), ex(null), console.log("✅ Permissions saved successfully")
              } catch (e) {
                console.error("❌ Error saving permissions:", e), w(e instanceof Error ? e.message : "Failed to save permissions")
              } finally {
                eu(!1)
              }
            }
          }, eR = async e => {
            er(e => ({
              ...e,
              loading: !0
            }));
            try {
              let t = await fetch("".concat("", "/api/objects/").concat(e), {
                method: "DELETE"
              });
              if (!t.ok) throw Error("Failed to delete object: ".concat(t.statusText));
              await ek(), er({
                isOpen: !1,
                object: null,
                loading: !1
              })
            } catch (e) {
              w(e instanceof Error ? e.message : "Failed to delete object"), er(e => ({
                ...e,
                loading: !1
              }))
            }
          }, eI = async () => {
            er(e => ({
              ...e,
              loading: !0
            }));
            try {
              let e = I.filter(e => V.has(e.uid)).map(e => fetch("".concat("", "/api/objects/").concat(e.uid), {
                  method: "DELETE"
                })),
                t = (await Promise.all(e)).filter(e => !e.ok);
              if (t.length > 0) throw Error("Failed to delete ".concat(t.length, " objects"));
              q(new Set), J(!1), await ek(), er({
                isOpen: !1,
                object: null,
                loading: !1
              })
            } catch (e) {
              w(e instanceof Error ? e.message : "Failed to delete objects"), er(e => ({
                ...e,
                loading: !1
              }))
            }
          };
        (0, l.useEffect)(() => {
          let t = e;
          _ && (t = e.filter(e => e_(e, _))), S && (t = t.filter(e => e.email.toLowerCase().includes(S.toLowerCase())));
          let s = eZ(t, F, M);
          B(s), P(s.length), ea(Math.ceil(s.length / ee)), (_ !== G || S !== K) && (q(new Set), J(!1), H(_), Y(S))
        }, [e, F, M, _, S, eZ, ee, G, K]);
        let eB = e => {
            if (!e) return "N/A";
            try {
              return new Date(e).toLocaleString()
            } catch (e) {
              return "Invalid date"
            }
          },
          eW = e => {
            if (!e) return !1;
            try {
              let t = new Date(e).getTime();
              return (new Date().getTime() - t) / 1e3 < 10
            } catch (e) {
              return !1
            }
          };
        return ((0, l.useEffect)(() => {
          (async () => {
            g(!0), await Promise.all([ew(), ek()]), g(!1)
          })()
        }, []), (0, l.useEffect)(() => {
          if (!W) return;
          let e = setInterval(() => {
            ek()
          }, 1e3);
          return () => clearInterval(e)
        }, [W]), (0, l.useEffect)(() => {
          O > 0 && ea(Math.ceil(O / ee))
        }, [O, ee]), (0, l.useEffect)(() => {
          // Drag and drop functionality
          const handleDragOver = (e) => {
            e.preventDefault();
            e.stopPropagation();
            e.dataTransfer.dropEffect = 'copy';
          };
          
          const handleDragEnter = (e) => {
            e.preventDefault();
            e.stopPropagation();
            // Create magical rainbow overlay
            let overlay = document.getElementById('drag-overlay');
            if (!overlay) {
              overlay = document.createElement('div');
              overlay.id = 'drag-overlay';
              overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, #ff0080, #ff8c00, #40e0d0, #9400d3, #ff1493, #00ff7f, #1e90ff, #ff69b4);
                background-size: 400% 400%;
                animation: rainbow-pulse 2s ease-in-out infinite;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                backdrop-filter: blur(2px);
                opacity: 0;
                transition: opacity 0.3s ease;
              `;
              
              overlay.innerHTML = `
                <style>
                  @keyframes rainbow-pulse {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                  }
                  @keyframes bounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-30px); }
                    60% { transform: translateY(-15px); }
                  }
                  @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                  }
                  .bounce { animation: bounce 2s infinite; }
                  .spin { animation: spin 3s linear infinite; }
                </style>
                <div style="text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                  <div class="spin" style="margin-bottom: 20px;">
                    <svg width="120" height="140" viewBox="0 0 311 360" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <g clip-path="url(#clip0_drag)">
                        <path d="M311.414 89.7878L155.518 179.998L-0.378906 89.7878L155.518 -0.422485L311.414 89.7878Z" fill="url(#paint0_linear_drag)"></path>
                        <path d="M311.414 89.7878V270.208L155.518 360.423V179.998L311.414 89.7878Z" fill="url(#paint1_linear_drag)"></path>
                        <path d="M155.518 179.998V360.423L-0.378906 270.208V89.7878L155.518 179.998Z" fill="url(#paint2_linear_drag)"></path>
                      </g>
                      <defs>
                        <linearGradient id="paint0_linear_drag" x1="155.518" y1="-0.422485" x2="155.518" y2="179.998" gradientUnits="userSpaceOnUse">
                          <stop stop-color="#FFFFFF"/>
                          <stop offset="1" stop-color="#E0E7FF"/>
                        </linearGradient>
                        <linearGradient id="paint1_linear_drag" x1="233.466" y1="89.7878" x2="233.466" y2="360.423" gradientUnits="userSpaceOnUse">
                          <stop stop-color="#C7D2FE"/>
                          <stop offset="1" stop-color="#A5B4FC"/>
                        </linearGradient>
                        <linearGradient id="paint2_linear_drag" x1="77.5696" y1="89.7878" x2="77.5696" y2="360.423" gradientUnits="userSpaceOnUse">
                          <stop stop-color="#E0E7FF"/>
                          <stop offset="1" stop-color="#C7D2FE"/>
                        </linearGradient>
                        <clipPath id="clip0_drag">
                          <rect width="311" height="360" fill="white" transform="translate(-0.378906 0.00488281)"/>
                        </clipPath>
                      </defs>
                    </svg>
                  </div>
                  <div class="bounce" style="font-size: 48px; margin-bottom: 20px;">
                    🦄✨🌈
                  </div>
                  <h2 style="font-size: 32px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 3px;">
                    Drop Your File Here!
                  </h2>
                  <p style="font-size: 18px; opacity: 0.9;">
                    🦙 Ready to create magical SyftObjects! 🦙
                  </p>
                  <div style="margin-top: 20px; font-size: 24px;">
                    ✨ 🌟 ⭐ 💫 ⚡ 🌈 ✨
                  </div>
                </div>
              `;
              
              document.body.appendChild(overlay);
            }
            
            // Fade in the overlay
            requestAnimationFrame(() => {
              overlay.style.opacity = '0.95';
            });
          };
          
          const handleDragLeave = (e) => {
            e.preventDefault();
            e.stopPropagation();
            // Only remove visual feedback if we're actually leaving the document
            if (e.clientX === 0 && e.clientY === 0) {
              const overlay = document.getElementById('drag-overlay');
              if (overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => {
                  if (overlay.parentNode) {
                    overlay.parentNode.removeChild(overlay);
                  }
                }, 300);
              }
            }
          };
          
          const handleDrop = (e) => {
            e.preventDefault();
            e.stopPropagation();
            // Remove magical overlay
            const overlay = document.getElementById('drag-overlay');
            if (overlay) {
              overlay.style.opacity = '0';
              setTimeout(() => {
                if (overlay.parentNode) {
                  overlay.parentNode.removeChild(overlay);
                }
              }, 300);
            }
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
              const file = files[0];
              
              // Find and click the "New" button to open the enhanced modal
              const newButtons = document.querySelectorAll('button');
              let newButton = null;
              for (let button of newButtons) {
                if (button.textContent && button.textContent.trim() === 'New') {
                  newButton = button;
                  break;
                }
              }
              
              if (newButton) {
                console.log('🎯 Found New button, clicking it...');
                newButton.click();
                
                // Wait for the modal to be created, then populate it with the dropped file
                setTimeout(() => {
                  console.log('📁 Populating modal with dropped file:', file.name);
                  
                  // Pre-populate the object name (remove file extension)
                  const nameField = document.querySelector('[name="name"]');
                  if (nameField) {
                    nameField.value = file.name.replace(/\.[^/.]+$/, '');
                    console.log('📝 Set name:', nameField.value);
                  }
                  
                  // Pre-populate the description
                  const descField = document.querySelector('[name="description"]');
                  if (descField) {
                    descField.value = `Auto-generated object: ${file.name.replace(/\.[^/.]+$/, '')}`;
                    console.log('📝 Set description:', descField.value);
                  }
                  
                  // Read the file content and populate the private content field
                  const reader = new FileReader();
                  reader.onload = function(e) {
                    console.log('📖 File read complete, populating content...');
                    
                    // Find the private paste content field
                    const privateContentField = document.querySelector('[name="privateFileContent"]');
                    if (privateContentField) {
                      const fileContent = e.target.result;
                      const preview = fileContent.length > 1000 ? 
                        fileContent.substring(0, 1000) + '\n... (file truncated for preview, full content will be uploaded)' : 
                        fileContent;
                      
                      privateContentField.value = preview;
                      console.log('📝 Set private content preview:', preview.substring(0, 100) + '...');
                      
                      // Store full content in hidden field
                      const form = document.getElementById('new-object-form');
                      if (form) {
                        let fullContentField = form.querySelector('[name="fullPrivateFileContent"]');
                        if (!fullContentField) {
                          fullContentField = document.createElement('input');
                          fullContentField.type = 'hidden';
                          fullContentField.name = 'fullPrivateFileContent';
                          form.appendChild(fullContentField);
                          console.log('🆕 Created hidden field for full content');
                        }
                        fullContentField.value = fileContent;
                        console.log('💾 Stored full content, length:', fileContent.length);
                        
                        // Store filename
                        let filenameField = form.querySelector('[name="privateFilename"]');
                        if (!filenameField) {
                          filenameField = document.createElement('input');
                          filenameField.type = 'hidden';
                          filenameField.name = 'privateFilename';
                          form.appendChild(filenameField);
                        }
                        filenameField.value = file.name;
                        console.log('💾 Stored filename:', file.name);
                      }
                      
                      // Switch to the paste tab to show the content
                      const privatePasteTab = document.getElementById('private-paste-tab');
                      if (privatePasteTab) {
                        privatePasteTab.click();
                        console.log('🔄 Switched to paste tab');
                      }
                    }
                  };
                  reader.readAsText(file);
                }, 200); // Give the modal time to be created
              } else {
                console.error('❌ Could not find New button');
                // Fallback - show a simple alert
                alert('Could not find New button to open the modal. Please try clicking the New button manually and then drag the file again.');
              }
            }
          };
          
          // Add event listeners to document
          document.addEventListener('dragover', handleDragOver);
          document.addEventListener('dragenter', handleDragEnter);
          document.addEventListener('dragleave', handleDragLeave);
          document.addEventListener('drop', handleDrop);
          
          // Cleanup function
          return () => {
            document.removeEventListener('dragover', handleDragOver);
            document.removeEventListener('dragenter', handleDragEnter);
            document.removeEventListener('dragleave', handleDragLeave);
            document.removeEventListener('drop', handleDrop);
          };
        }, []), s) ? (0, a.jsx)("div", {
          className: "flex items-center justify-center min-h-screen p-4",
          style: {background: "#ffffff"},
          children: (0, a.jsxs)("div", {
            className: "text-center space-y-32",
            children: [(0, a.jsx)(j, {
              className: "h-48 w-48 mx-auto",
              isLoading: !0
            }), (0, a.jsx)("p", {
              className: "text-3xl font-bold tracking-wide text-gray-600",
              style: {marginTop: "100px"},
              children: "the internet of private data"
            })]
          })
        }) : (0, a.jsxs)("div", {
          className: "h-full bg-background text-foreground flex flex-col overflow-hidden",
          children: [(0, a.jsxs)("div", {
            className: "flex-shrink-0 space-y-3 p-0",
            children: [(0, a.jsx)("div", {
              className: "bg-card rounded border p-2",
              children: (0, a.jsxs)("div", {
                className: "flex flex-col sm:flex-row gap-1",
                children: [(0, a.jsx)("div", {
                  className: "flex-1",
                  children: (0, a.jsxs)("div", {
                    className: "relative",
                    children: [(0, a.jsx)(n.Z, {
                      className: "absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground"
                    }), (0, a.jsx)("input", {
                      type: "text",
                      placeholder: "Search objects...",
                      value: _,
                      onChange: e => D(e.target.value),
                      onKeyPress: e => "Enter" === e.key && eC(),
                      className: "w-full pl-7 pr-2 py-1 border rounded text-xs focus:ring-1 focus:ring-primary focus:border-transparent"
                    })]
                  })
                }), (0, a.jsx)("div", {
                  className: "flex-1",
                  children: (0, a.jsxs)("div", {
                    className: "relative",
                    children: [(0, a.jsx)(i.Z, {
                      className: "absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground"
                    }), (0, a.jsx)("input", {
                      type: "text",
                      placeholder: "Filter by Admin...",
                      value: S,
                      onChange: e => E(e.target.value),
                      onKeyPress: e => "Enter" === e.key && eC(),
                      className: "w-full pl-7 pr-2 py-1 border rounded text-xs focus:ring-1 focus:ring-primary focus:border-transparent"
                    })]
                  })
                }), (0, a.jsxs)("div", {
                  className: "flex space-x-1",
                  children: [(0, a.jsx)("button", {
                    onClick: eC,
                    className: "px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs hover:bg-blue-200",
                    children: "Search"
                  }), (0, a.jsx)("button", {
                    onClick: () => {
                      D(""), E(""), X(1), q(new Set), J(!1)
                    },
                    className: "px-2 py-1 bg-secondary text-secondary-foreground rounded text-xs hover:bg-secondary/90",
                    children: "Clear"
                  }), (0, a.jsx)("button", {
                    onClick: () => {
                      // Create and show comprehensive new object modal
                      let existingModal = document.getElementById('new-object-modal');
                      if (existingModal) {
                        existingModal.remove();
                      }
                      
                      const modal = document.createElement('div');
                      modal.id = 'new-object-modal';
                                              modal.className = 'fixed inset-0 flex items-center justify-center p-2 z-50';
                      modal.style.paddingTop = '0';
                      modal.style.paddingBottom = '30px';
                      modal.style.paddingLeft = '25px';
                      modal.style.paddingRight = '25px';
                        modal.innerHTML = `
                          <div class="bg-white rounded-xl w-full" style="max-width: 1142px; max-height: 90%; height: 90%; position: relative; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #e2e8f0;">
                            <div class="px-6 py-4 border-b flex-shrink-0 rounded-t-xl bg-gradient-to-r from-slate-50 to-gray-50">
                              <div class="flex items-center justify-between">
                                <h2 class="text-xl font-semibold text-gray-800">✨ Create New SyftObject</h2>
                                <button id="close-modal" class="text-gray-400 hover:text-gray-600 text-xl font-bold rounded-full w-8 h-8 flex items-center justify-center hover:bg-gray-100 transition-colors">✕</button>
                              </div>
                            </div>
                            <div class="overflow-y-auto p-6" style="height: calc(100% - 140px); padding-bottom: 20px;">
                              <form id="new-object-form" class="space-y-6">
                                <!-- Basic Info Section -->
                                <div class="grid grid-cols-2 gap-6">
                                  <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">🎯 Object Name</label>
                                    <input type="text" name="name" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition-all" value="Syft Object" style="background: #fafbfc;">
                                  </div>
                                  <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">📧 Admin Email</label>
                                    <input type="email" name="email" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition-all" value="" style="background: #fafbfc;">
                                  </div>
                                </div>
                                
                                <!-- Description Section -->
                                <div>
                                  <label class="block text-sm font-medium text-gray-700 mb-1">📝 Description</label>
                                  <textarea name="description" rows="4" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition-all" style="background: #fafbfc;">Auto-generated object: Syft Object</textarea>
                                </div>
                                                                                              <!-- File Content Section -->
                                <div class="grid grid-cols-2 gap-6">
                                  <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">🔒 Private File Content</label>
                                    <div class="border border-gray-200 rounded-lg bg-green-50/30">
                                      <div class="flex border-b border-gray-200">
                                        <button type="button" id="private-upload-tab" class="px-4 py-2 text-sm font-medium text-green-700 border-b-2 border-green-500 bg-green-50 rounded-tl-lg">📁 Upload File</button>
                                        <button type="button" id="private-paste-tab" class="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-50">✏️ Paste Content</button>
                                      </div>
                                      <div id="private-upload-content" class="p-4">
                                        <input type="file" name="privateFile" id="private-file-upload" class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-green-50 file:text-green-700 hover:file:bg-green-100">
                                        <p class="text-xs text-gray-500 mt-2">📊 Upload private data file (CSV, JSON, Python, etc.)</p>
                                      </div>
                                      <div id="private-paste-content" class="p-4 hidden">
                                        <textarea name="privateFileContent" rows="4" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-400 focus:border-green-400 transition-all" style="background: #fafbfc;">Auto-generated private content for Syft Object</textarea>
                                      </div>
                                    </div>
                                  </div>
                                  <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">🎭 Mock File Content</label>
                                    <div class="border border-gray-200 rounded-lg bg-blue-50/30">
                                      <div class="flex border-b border-gray-200">
                                        <button type="button" id="mock-upload-tab" class="px-4 py-2 text-sm font-medium text-blue-700 border-b-2 border-blue-500 bg-blue-50 rounded-tl-lg">📁 Upload File</button>
                                        <button type="button" id="mock-paste-tab" class="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-50">✏️ Paste Content</button>
                                      </div>
                                      <div id="mock-upload-content" class="p-4">
                                        <input type="file" name="mockFile" id="mock-file-upload" class="w-full text-sm text-gray-600 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
                                        <p class="text-xs text-gray-500 mt-2">🎨 Upload mock/synthetic data file (CSV, JSON, Python, etc.)</p>
                                      </div>
                                      <div id="mock-paste-content" class="p-4 hidden">
                                        <textarea name="mockFileContent" rows="4" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all" style="background: #fafbfc;">Auto-generated mock content for Syft Object</textarea>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                                
                                <!-- Metadata Section -->
                                <div>
                                  <label class="block text-sm font-medium text-gray-700 mb-1">⚙️ Metadata (JSON format)</label>
                                  <textarea name="metadata" rows="3" class="w-full px-4 py-3 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 font-mono transition-all bg-orange-50/30" placeholder="{}">{}</textarea>
                                </div>
                                                                                               <!-- Permissions Section -->
                                <div>
                                  <label class="block text-sm font-medium text-gray-700 mb-3">🔐 Permissions</label>
                                  <div class="bg-purple-50/30 p-4 rounded-lg space-y-4">
                                    <div class="grid grid-cols-2 gap-6">
                                      <div class="permission-group" data-permission="private_read">
                                        <label class="block text-xs font-medium text-gray-700 mb-2">🔒 Private Read</label>
                                        <div class="permission-emails space-y-2"></div>
                                        <button type="button" class="add-permission-btn mt-2 px-3 py-1 text-xs bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-all">+ Add Email</button>
                                      </div>
                                      <div class="permission-group" data-permission="private_write">
                                        <label class="block text-xs font-medium text-gray-700 mb-2">✏️ Private Write</label>
                                        <div class="permission-emails space-y-2"></div>
                                        <button type="button" class="add-permission-btn mt-2 px-3 py-1 text-xs bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-all">+ Add Email</button>
                                      </div>
                                    </div>
                                    <div class="grid grid-cols-2 gap-6">
                                      <div class="permission-group" data-permission="mock_read">
                                        <label class="block text-xs font-medium text-gray-700 mb-2">👁️ Mock Read</label>
                                        <div class="permission-emails space-y-2"></div>
                                        <button type="button" class="add-permission-btn mt-2 px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-all">+ Add Email</button>
                                      </div>
                                      <div class="permission-group" data-permission="mock_write">
                                        <label class="block text-xs font-medium text-gray-700 mb-2">📝 Mock Write</label>
                                        <div class="permission-emails space-y-2"></div>
                                        <button type="button" class="add-permission-btn mt-2 px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-all">+ Add Email</button>
                                      </div>
                                    </div>
                                    <div class="permission-group" data-permission="syftobject">
                                      <label class="block text-xs font-medium text-gray-700 mb-2">🌟 SyftObject Access</label>
                                      <div class="permission-emails space-y-2"></div>
                                      <button type="button" class="add-permission-btn mt-2 px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-all">+ Add Email</button>
                                    </div>
                                  </div>
                                </div>
                            </form>
                          </div>
                                                     <div class="px-6 py-4 border-t flex-shrink-0 rounded-b-xl bg-gradient-to-r from-slate-50 to-gray-50" style="position: absolute; bottom: 0; left: 0; right: 0;">
                             <div class="flex justify-end gap-4">
                               <button id="cancel-btn" class="px-6 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-gray-400 transition-all">🚫 Cancel</button>
                               <button id="create-btn" class="px-6 py-2 text-sm font-bold text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-200 shadow-md" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);">✨ Create Object</button>
                             </div>
                           </div>
                        </div>
                      `;
                      
                      document.body.appendChild(modal);
                      
                      // Permission management functions
                      function addEmailToPermission(permissionType, email = '') {
                        const group = document.querySelector(`[data-permission="${permissionType}"]`);
                        const emailsContainer = group.querySelector('.permission-emails');
                        
                        const emailDiv = document.createElement('div');
                        emailDiv.className = 'flex items-center gap-2';
                        emailDiv.innerHTML = `
                          <input type="text" 
                                 class="flex-1 px-2 py-1 text-xs border border-gray-200 rounded focus:ring-1 focus:ring-indigo-400 focus:border-indigo-400 transition-all" 
                                 style="background: #fafbfc;" 
                                 value="${email}"
                                 placeholder="email@example.com or 'public'">
                          <button type="button" class="remove-email-btn px-2 py-1 text-xs bg-red-100 text-red-600 rounded hover:bg-red-200 transition-all">×</button>
                        `;
                        
                        emailsContainer.appendChild(emailDiv);
                        
                        // Add remove functionality
                        emailDiv.querySelector('.remove-email-btn').onclick = () => emailDiv.remove();
                        
                        // Focus the new input
                        emailDiv.querySelector('input').focus();
                      }
                      
                      function collectPermissions() {
                        const permissions = {};
                        document.querySelectorAll('.permission-group').forEach(group => {
                          const permissionType = group.dataset.permission;
                          const emails = [];
                          group.querySelectorAll('.permission-emails input').forEach(input => {
                            const email = input.value.trim();
                            if (email) emails.push(email);
                          });
                          permissions[permissionType] = emails;
                        });
                        return permissions;
                      }
                      
                      // Fetch client info and populate defaults
                      fetch('/api/client-info')
                        .then(response => response.json())
                        .then(data => {
                          const defaults = data.defaults;
                          // Set admin email
                          document.querySelector('[name="email"]').value = defaults.admin_email;
                          
                          // Set permission defaults using the new system
                          addEmailToPermission('private_read', defaults.permissions.private_read);
                          addEmailToPermission('private_write', defaults.permissions.private_write);
                          addEmailToPermission('mock_read', 'public');
                          addEmailToPermission('mock_write', defaults.permissions.mock_write);
                          addEmailToPermission('syftobject', 'public');
                        })
                        .catch(err => console.log('Could not load client info:', err));
                      
                      // Add event listeners
                      document.getElementById('close-modal').onclick = () => modal.remove();
                      document.getElementById('cancel-btn').onclick = () => modal.remove();
                      modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
                      
                      // Add permission button listeners
                      document.querySelectorAll('.add-permission-btn').forEach(btn => {
                        btn.onclick = () => {
                          const permissionType = btn.closest('.permission-group').dataset.permission;
                          addEmailToPermission(permissionType);
                        };
                      });
                      
                                              // Auto-update description and content when name changes
                        document.querySelector('[name="name"]').oninput = function() {
                          const descField = document.querySelector('[name="description"]');
                          const privateContentField = document.querySelector('[name="privateFileContent"]');
                          const mockContentField = document.querySelector('[name="mockFileContent"]');
                          const name = this.value || 'Syft Object';
                          descField.value = `Auto-generated object: ${name}`;
                          privateContentField.value = `Auto-generated private content for ${name}`;
                          mockContentField.value = `Auto-generated mock content for ${name}`;
                        };
                        
                                                 // Private file tab switching
                         document.getElementById('private-upload-tab').onclick = function() {
                           this.className = 'px-3 py-1 text-xs font-medium text-green-600 border-b-2 border-green-600';
                           document.getElementById('private-paste-tab').className = 'px-3 py-1 text-xs font-medium text-gray-500 hover:text-gray-700';
                           document.getElementById('private-upload-content').classList.remove('hidden');
                           document.getElementById('private-paste-content').classList.add('hidden');
                         };
                         document.getElementById('private-paste-tab').onclick = function() {
                           this.className = 'px-3 py-1 text-xs font-medium text-green-600 border-b-2 border-green-600';
                           document.getElementById('private-upload-tab').className = 'px-3 py-1 text-xs font-medium text-gray-500 hover:text-gray-700';
                           document.getElementById('private-paste-content').classList.remove('hidden');
                           document.getElementById('private-upload-content').classList.add('hidden');
                         };
                        
                                                 // Mock file tab switching
                         document.getElementById('mock-upload-tab').onclick = function() {
                           this.className = 'px-3 py-1 text-xs font-medium text-blue-600 border-b-2 border-blue-600';
                           document.getElementById('mock-paste-tab').className = 'px-3 py-1 text-xs font-medium text-gray-500 hover:text-gray-700';
                           document.getElementById('mock-upload-content').classList.remove('hidden');
                           document.getElementById('mock-paste-content').classList.add('hidden');
                         };
                         document.getElementById('mock-paste-tab').onclick = function() {
                           this.className = 'px-3 py-1 text-xs font-medium text-blue-600 border-b-2 border-blue-600';
                           document.getElementById('mock-upload-tab').className = 'px-3 py-1 text-xs font-medium text-gray-500 hover:text-gray-700';
                           document.getElementById('mock-paste-content').classList.remove('hidden');
                           document.getElementById('mock-upload-content').classList.add('hidden');
                         };
                      
                                              // Private file upload handler
                        document.getElementById('private-file-upload').onchange = function(e) {
                          console.log('🔥 Private file upload triggered');
                          const file = e.target.files[0];
                          if (file) {
                            console.log('📁 File selected:', file.name, 'Size:', file.size);
                            const reader = new FileReader();
                            reader.onload = function(e) {
                              console.log('📖 File read complete');
                              const form = document.getElementById('new-object-form');
                              let fileContentField = form.querySelector('[name="privateFileContent"]');
                              let filenameField = form.querySelector('[name="privateFilename"]');
                              
                              // Store original filename
                              if (!filenameField) {
                                filenameField = document.createElement('input');
                                filenameField.type = 'hidden';
                                filenameField.name = 'privateFilename';
                                form.appendChild(filenameField);
                              }
                              filenameField.value = file.name;
                              console.log('💾 Stored filename:', file.name);
                              
                              // Only show first 1000 characters in preview
                              const content = e.target.result;
                              console.log('📝 File content length:', content.length);
                              console.log('📝 File content preview:', content.substring(0, 100) + '...');
                              const preview = content.length > 1000 ? 
                                content.substring(0, 1000) + '\\n... (file truncated for preview, full content will be uploaded)' : 
                                content;
                              
                              if (fileContentField) {
                                fileContentField.value = preview;
                                console.log('👁️ Set preview in visible field');
                                // Store full content in hidden field
                                let fullContentField = form.querySelector('[name="fullPrivateFileContent"]');
                                if (!fullContentField) {
                                  fullContentField = document.createElement('textarea');
                                  fullContentField.style.display = 'none';
                                  fullContentField.name = 'fullPrivateFileContent';
                                  form.appendChild(fullContentField);
                                  console.log('🆕 Created hidden field for full content');
                                }
                                fullContentField.value = content;
                                console.log('💾 Stored full content in hidden field, length:', content.length);
                              }
                              // Auto-switch to paste tab to show the content
                              document.getElementById('private-paste-tab').click();
                            };
                            reader.readAsText(file);
                          }
                        };
                        
                        // Mock file upload handler
                        document.getElementById('mock-file-upload').onchange = function(e) {
                          console.log('🔥 Mock file upload triggered');
                          const file = e.target.files[0];
                          if (file) {
                            console.log('📁 Mock file selected:', file.name, 'Size:', file.size);
                            const reader = new FileReader();
                            reader.onload = function(e) {
                              console.log('📖 Mock file read complete');
                              const form = document.getElementById('new-object-form');
                              let fileContentField = form.querySelector('[name="mockFileContent"]');
                              let filenameField = form.querySelector('[name="mockFilename"]');
                              
                              // Store original filename
                              if (!filenameField) {
                                filenameField = document.createElement('input');
                                filenameField.type = 'hidden';
                                filenameField.name = 'mockFilename';
                                form.appendChild(filenameField);
                              }
                              filenameField.value = file.name;
                              console.log('💾 Stored mock filename:', file.name);
                              
                              // Only show first 1000 characters in preview
                              const content = e.target.result;
                              console.log('📝 Mock file content length:', content.length);
                              console.log('📝 Mock file content preview:', content.substring(0, 100) + '...');
                              const preview = content.length > 1000 ? 
                                content.substring(0, 1000) + '\\n... (file truncated for preview, full content will be uploaded)' : 
                                content;
                              
                              if (fileContentField) {
                                fileContentField.value = preview;
                                console.log('👁️ Set mock preview in visible field');
                                // Store full content in hidden field
                                let fullContentField = form.querySelector('[name="fullMockFileContent"]');
                                if (!fullContentField) {
                                  fullContentField = document.createElement('textarea');
                                  fullContentField.style.display = 'none';
                                  fullContentField.name = 'fullMockFileContent';
                                  form.appendChild(fullContentField);
                                  console.log('🆕 Created hidden field for mock full content');
                                }
                                fullContentField.value = content;
                                console.log('💾 Stored mock full content in hidden field, length:', content.length);
                              }
                              // Auto-switch to paste tab to show the content
                              document.getElementById('mock-paste-tab').click();
                            };
                            reader.readAsText(file);
                          }
                        };
                      
                      // Form submission
                      document.getElementById('create-btn').onclick = async function() {
                        const form = document.getElementById('new-object-form');
                        const formData = new FormData(form);
                        const data = Object.fromEntries(formData.entries());
                        
                        // Get file content from hidden fields or visible fields
                        const fullPrivateField = form.querySelector('[name="fullPrivateFileContent"]');
                        const fullMockField = form.querySelector('[name="fullMockFileContent"]');
                        
                        const privateFileContent = (fullPrivateField && fullPrivateField.value) || 
                                                  data.privateFileContent || '';
                        const privateFilename = (form.querySelector('[name="privateFilename"]') && 
                                               form.querySelector('[name="privateFilename"]').value) || '';
                        const mockFileContent = (fullMockField && fullMockField.value) || 
                                              data.mockFileContent || '';
                        const mockFilename = (form.querySelector('[name="mockFilename"]') && 
                                           form.querySelector('[name="mockFilename"]').value) || '';
                        
                        console.log('🚀 Form submission debug:', {
                          privateFileContent: privateFileContent.substring(0, 200) + '...',
                          privateFilename,
                          mockFileContent: mockFileContent.substring(0, 200) + '...',
                          mockFilename,
                          hasFullPrivateField: !!fullPrivateField,
                          hasFullMockField: !!fullMockField,
                          fullPrivateLength: fullPrivateField ? fullPrivateField.value.length : 0,
                          fullMockLength: fullMockField ? fullMockField.value.length : 0,
                          visiblePrivateValue: data.privateFileContent ? data.privateFileContent.substring(0, 100) + '...' : 'empty',
                          visibleMockValue: data.mockFileContent ? data.mockFileContent.substring(0, 100) + '...' : 'empty'
                        });
                        
                        // Note: name is optional - syobj will auto-generate if empty
                        
                        // Process permissions using the new collection system
                        const permissions = collectPermissions();
                        
                        // Parse metadata
                        let metadata = {};
                        if (data.metadata) {
                          try {
                            metadata = JSON.parse(data.metadata);
                          } catch (e) {
                            alert('Invalid JSON in metadata field');
                            return;
                          }
                        }
                        
                        const objData = {
                          name: data.name,
                          description: data.description || '',
                          email: data.email || '',
                          private_file_content: privateFileContent,
                          private_filename: privateFilename,
                          mock_file_content: mockFileContent,
                          mock_filename: mockFilename,
                          metadata: metadata,
                          permissions: permissions
                        };
                        
                        try {
                          this.textContent = 'Creating...';
                          this.disabled = true;
                          
                          const response = await fetch('/api/objects', {
                            method: 'POST',
                            headers: {
                              'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(objData)
                          });
                          
                          if (response.ok) {
                            modal.remove();
                            // Refresh the objects list
                            ek();
                            eN('SyftObject created successfully!');
                          } else {
                            const error = await response.text();
                            alert('Error creating object: ' + error);
                          }
                        } catch (error) {
                          alert('Error creating object: ' + error.message);
                        } finally {
                          this.textContent = 'Create Object';
                          this.disabled = false;
                        }
                      };
                    },
                    className: "px-2 py-1 bg-green-100 text-green-800 rounded text-xs hover:bg-green-200",
                    children: "New"
                  }), V.size > 0 && (0, a.jsx)(a.Fragment, {
                    children: [(0, a.jsxs)("button", {
                      onClick: () => {
                        0 !== I.filter(e => V.has(e.uid)).length && er({
                          isOpen: !0,
                          object: null,
                          loading: !1
                        })
                      },
                      className: "px-2 py-1 bg-red-100 text-red-800 rounded text-xs hover:bg-red-200",
                      children: ["Delete Selected (", V.size, ")"]
                    }), (0, a.jsx)("button", {
                      onClick: () => {
                        let e = I.filter(e => V.has(e.uid)).map(e => `syo.objects["${e.uid}"]`),
                          t = Math.floor(Math.random() * 100),
                          s = `results_${t} = [${e.join(", ")}]`;
                        (async () => {
                          try {
                            if (navigator.clipboard && navigator.clipboard.writeText) {
                              try {
                                await navigator.clipboard.writeText(s);
                                eN(e.length > 1 ? "Python code for syft objects copied to clipboard" : s);
                                return
                              } catch (err) {
                                console.log("Modern clipboard failed, trying fallback:", err)
                              }
                            }
                            let t = document.createElement("textarea");
                            t.value = s;
                            t.style.position = "fixed";
                            t.style.left = "-999999px";
                            t.style.top = "-999999px";
                            t.style.width = "1px";
                            t.style.height = "1px";
                            t.style.opacity = "0";
                            t.setAttribute("readonly", "");
                            document.body.appendChild(t);
                            try {
                              t.focus();
                              t.select();
                              t.setSelectionRange(0, s.length);
                              let success = document.execCommand("copy");
                              document.body.removeChild(t);
                              if (success) {
                                eN(e.length > 1 ? "Python code for syft objects copied to clipboard" : s)
                              } else {
                                throw new Error("execCommand failed")
                              }
                            } catch (err) {
                              document.body.removeChild(t);
                              throw err
                            }
                          } catch (finalErr) {
                            console.error("All clipboard methods failed:", finalErr);
                            eN("Failed to copy to clipboard")
                          }
                        })()
                      },
                      className: "px-2 py-1 bg-green-100 text-green-800 rounded text-xs hover:bg-green-200",
                      title: "Copy selected objects as Python variable",
                      children: "Python"
                    })]
                  }), (0, a.jsx)("button", {
                    onClick: eD,
                    className: "px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs hover:bg-blue-200",
                    children: $ ? "Deselect All" : "Select All"
                  }), (0, a.jsx)("button", {
                    onClick: () => window.open("/", "_blank"),
                    className: "px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs hover:bg-gray-200",
                    title: "Open widget in separate window",
                    children: "Open in Window"
                  }), (0, a.jsx)("button", {
                    onClick: () => {
                      if (window.confirm("Are you sure you want to reload the widget? Continue?")) {
                        fetch("/api/syftbox/reinstall", {
                          method: "POST"
                        }).catch(() => {});
                        document.body.innerHTML = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:white;display:flex;align-items:center;justify-content:center;font-family:system-ui,sans-serif;z-index:9999;padding:20px;box-sizing:border-box"><div style="text-align:center;max-width:400px;width:100%"><div style="margin-bottom:40px;display:flex;justify-content:center"><svg width="100" height="116" viewBox="0 0 311 360" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_reload)"><path d="M311.414 89.7878L155.518 179.998L-0.378906 89.7878L155.518 -0.422485L311.414 89.7878Z" fill="url(#paint0_linear_reload)"></path><path d="M311.414 89.7878V270.208L155.518 360.423V179.998L311.414 89.7878Z" fill="url(#paint1_linear_reload)"></path><path d="M155.518 179.998V360.423L-0.378906 270.208V89.7878L155.518 179.998Z" fill="url(#paint2_linear_reload)"></path></g><defs><linearGradient id="paint0_linear_reload" x1="-0.378904" y1="89.7878" x2="311.414" y2="89.7878" gradientUnits="userSpaceOnUse"><stop stop-color="#DC7A6E"></stop><stop offset="0.251496" stop-color="#F6A464"></stop><stop offset="0.501247" stop-color="#FDC577"></stop><stop offset="0.753655" stop-color="#EFC381"></stop><stop offset="1" stop-color="#B9D599"></stop></linearGradient><linearGradient id="paint1_linear_reload" x1="309.51" y1="89.7878" x2="155.275" y2="360.285" gradientUnits="userSpaceOnUse"><stop stop-color="#BFCD94"></stop><stop offset="0.245025" stop-color="#B2D69E"></stop><stop offset="0.504453" stop-color="#8DCCA6"></stop><stop offset="0.745734" stop-color="#5CB8B7"></stop><stop offset="1" stop-color="#4CA5B8"></stop></linearGradient><linearGradient id="paint2_linear_reload" x1="-0.378906" y1="89.7878" x2="155.761" y2="360.282" gradientUnits="userSpaceOnUse"><stop stop-color="#D7686D"></stop><stop offset="0.225" stop-color="#C64B77"></stop><stop offset="0.485" stop-color="#A2638E"></stop><stop offset="0.703194" stop-color="#758AA8"></stop><stop offset="1" stop-color="#639EAF"></stop></linearGradient><clipPath id="clip0_reload"><rect width="311" height="360" fill="white"></rect></clipPath></defs></svg></div><div style="font-size:24px;color:#333;font-weight:500;line-height:1.4;letter-spacing:-0.02em"><div>Widget stopped.</div><div style="margin-top:8px">Please re-run your cell.</div></div></div></div>'
                      }
                    },
                    className: "px-1 py-1 bg-gray-100 text-gray-800 rounded text-xs hover:bg-gray-200 ml-1",
                    title: "Reinstall SyftBox app (removes and re-downloads)",
                    children: "🔄"
                  })]
                })]
              })
            }), N && (0, a.jsx)("div", {
              className: "bg-destructive/10 border border-destructive/20 rounded p-2",
              children: (0, a.jsxs)("p", {
                className: "text-destructive text-xs font-medium",
                children: ["Error: ", N]
              })
            })]
          }), (0, a.jsx)("div", {
            className: "flex-1 flex flex-col min-h-0",
            children: (0, a.jsxs)("div", {
              className: "bg-card rounded border overflow-hidden flex-1 flex flex-col",
              children: [(0, a.jsx)("div", {
                className: "flex-1 overflow-auto",
                children: (0, a.jsx)("div", {
                  className: "overflow-x-auto",
                  children: (0, a.jsxs)("table", {
                    className: "w-full text-xs",
                    children: [(0, a.jsx)("thead", {
                      className: "bg-muted/50 border-b",
                      children: (0, a.jsxs)("tr", {
                        children: [(0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium w-6",
                          children: (0, a.jsx)("input", {
                            type: "checkbox",
                            checked: $,
                            onChange: eD,
                            className: "h-3 w-3"
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-8",
                          onClick: () => eT("index"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "#"
                            }), "index" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-24",
                          onClick: () => eT("name"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "Name"
                            }), "name" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-32",
                          onClick: () => eT("description"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "Description"
                            }), "description" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-32",
                          onClick: () => eT("email"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "Admin"
                            }), "email" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-20",
                          onClick: () => eT("uid"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "UID"
                            }), "uid" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-28",
                          onClick: () => eT("created_at"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "Created"
                            }), "created_at" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-0 py-1.5 font-medium cursor-pointer hover:bg-muted/75 select-none w-10",
                          onClick: () => eT("type"),
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)("span", {
                              children: "Type"
                            }), "type" === F && ("desc" === M ? (0, a.jsx)(r.Z, {
                              className: "h-2 w-2"
                            }) : (0, a.jsx)(o.Z, {
                              className: "h-2 w-2"
                            }))]
                          })
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium w-20",
                          children: "Files"
                        }), (0, a.jsx)("th", {
                          className: "text-left px-1 py-1.5 font-medium w-40",
                          children: "Actions"
                        })]
                      })
                    }), (0, a.jsx)("tbody", {
                      children: 0 === I.length ? (0, a.jsx)("tr", {
                        children: (0, a.jsx)("td", {
                          colSpan: 10,
                          className: "px-2 py-4 text-center text-muted-foreground",
                          children: s ? "Loading..." : "No syft objects found"
                        })
                      }) : I.slice((Q - 1) * ee, Q * ee).map(e => (0, a.jsxs)("tr", {
                        className: "border-b transition-colors hover:bg-muted/50 cursor-pointer ".concat(eW(e.created_at) || eb.has(e.uid) ? "rainbow-bg" : ""),
                        onClick: t => {
                          if (t.target === t.currentTarget || t.target.closest("td:not(.actions-cell):not([data-no-click])")) {
                            let t = e.name.replace(/[^a-zA-Z0-9_]/g, "_").replace(/^[0-9]/, "_$&");
                            eA("".concat(t, ' = syo.objects["').concat(e.uid, '"]')), eg(t => new Set(t).add(e.uid)), setTimeout(() => {
                              eg(t => {
                                let s = new Set(t);
                                return s.delete(e.uid), s
                              })
                            }, 2e3)
                          }
                        },
                        children: [(0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-6",
                          "data-no-click": "true",
                          onClick: e => e.stopPropagation(),
                          children: (0, a.jsx)("input", {
                            type: "checkbox",
                            checked: V.has(e.uid),
                            onChange: () => eS(e.uid),
                            className: "h-3 w-3"
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-8",
                          children: e.index
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-24",
                          children: (0, a.jsx)("div", {
                            className: "font-medium truncate text-xs",
                            children: (0, a.jsx)("span", {
                              className: "text-foreground",
                              children: e.name
                            })
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-32",
                          children: (0, a.jsx)("div", {
                            className: "truncate text-xs text-muted-foreground",
                            children: e.description || "—"
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-32",
                          "data-no-click": "true",
                          children: (0, a.jsxs)("button", {
                            onClick: t => {
                              t.stopPropagation(), eA(e.email), ej(e.uid), setTimeout(() => ej(null), 2e3)
                            },
                            className: "flex items-center space-x-1 text-xs font-mono text-gray-700 hover:text-gray-900 cursor-pointer hover:bg-blue-100 hover:shadow-sm px-1 py-0.5 rounded truncate transition-all duration-500 border border-transparent hover:border-blue-200 w-full ".concat(ef === e.uid ? "bg-gradient-to-r from-red-100 via-orange-100 via-yellow-100 via-green-100 via-cyan-100 via-blue-100 to-purple-100 text-gray-800 border-purple-200" : ""),
                            title: "Click to copy admin email to clipboard",
                            children: [(0, a.jsx)(c.Z, {
                              className: "h-2 w-2 text-muted-foreground flex-shrink-0"
                            }), (0, a.jsx)("span", {
                              className: "truncate",
                              children: e.email
                            }), ef === e.email && (0, a.jsx)("span", {
                              className: "ml-1 text-green-700 font-semibold",
                              children: "✓"
                            })]
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-20",
                          "data-no-click": "true",
                          children: (0, a.jsxs)("button", {
                            onClick: t => {
                              t.stopPropagation(), eA(e.uid), eh(e.uid), setTimeout(() => eh(null), 2e3)
                            },
                            className: "text-xs font-mono text-gray-700 hover:text-gray-900 cursor-pointer hover:bg-blue-100 hover:shadow-sm px-1 py-0.5 rounded truncate transition-all duration-500 border border-transparent hover:border-blue-200 ".concat(ep === e.uid ? "bg-gradient-to-r from-red-100 via-orange-100 via-yellow-100 via-green-100 via-cyan-100 via-blue-100 to-purple-100 text-gray-800 border-purple-200" : ""),
                            title: "Click to copy full UID to clipboard",
                            children: [e.uid.substring(0, 8), "...", ep === e.uid && (0, a.jsx)("span", {
                              className: "ml-1 text-green-700 font-semibold",
                              children: "✓"
                            })]
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 text-muted-foreground w-28",
                          children: (0, a.jsxs)("div", {
                            className: "flex items-center space-x-1",
                            children: [(0, a.jsx)(d.Z, {
                              className: "h-2 w-2 flex-shrink-0"
                            }), (0, a.jsx)("span", {
                              className: "truncate text-xs",
                              children: eB(e.created_at)
                            })]
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-0 py-1.5 w-10",
                          children: (0, a.jsx)("div", {
                            className: "truncate text-xs",
                            children: (0, a.jsx)("span", {
                              className: "inline-flex items-center px-1 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800",
                              children: e.type || "—"
                            })
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-20",
                          "data-no-click": "true",
                          onClick: e => e.stopPropagation(),
                          children: (0, a.jsxs)("div", {
                            className: "flex space-x-0.5",
                            children: [e.file_exists.mock ? (0, a.jsxs)("button", {
                              onClick: () => {
                                var t;
                                let s = (null == k ? void 0 : null === (t = k.syftbox) || void 0 === t ? void 0 : t.user_email) || "",
                                  a = eU(e.uid),
                                  l = (null == a ? void 0 : a.mock_write.includes(s)) || !1;
                                eP(e.mock_url, "Mock: ".concat(e.name), "mock", e.uid, l)
                              },
                              className: "flex items-center space-x-0.5 px-1 py-0.5 rounded bg-slate-100 text-slate-700 hover:bg-slate-200 cursor-pointer text-xs",
                              title: "Edit mock file",
                              children: [(0, a.jsx)(x.Z, {
                                className: "h-2 w-2"
                              }), (0, a.jsx)("span", {
                                children: "Mock"
                              })]
                            }) : (0, a.jsxs)("div", {
                              className: "flex items-center space-x-0.5 px-1 py-0.5 rounded bg-slate-100 text-slate-700 opacity-50 text-xs",
                              children: [(0, a.jsx)(x.Z, {
                                className: "h-2 w-2"
                              }), (0, a.jsx)("span", {
                                children: "Mock"
                              })]
                            }), e.file_exists.private ? (0, a.jsxs)("button", {
                              onClick: () => {
                                var t;
                                let s = (null == k ? void 0 : null === (t = k.syftbox) || void 0 === t ? void 0 : t.user_email) || "",
                                  a = eU(e.uid),
                                  l = (null == a ? void 0 : a.private_write.includes(s)) || !1;
                                eP(e.private_url, "Private: ".concat(e.name), "private", e.uid, l)
                              },
                              className: "flex items-center space-x-0.5 px-1 py-0.5 rounded bg-gray-100 text-gray-700 hover:bg-gray-200 cursor-pointer text-xs",
                              title: "Edit private file",
                              children: [(0, a.jsx)(m.Z, {
                                className: "h-2 w-2"
                              }), (0, a.jsx)("span", {
                                children: "Private"
                              })]
                            }) : (0, a.jsxs)("div", {
                              className: "flex items-center space-x-0.5 px-1 py-0.5 rounded bg-gray-100 text-gray-600 opacity-50 text-xs",
                              children: [(0, a.jsx)(m.Z, {
                                className: "h-2 w-2"
                              }), (0, a.jsx)("span", {
                                children: "Private"
                              })]
                            })]
                          })
                        }), (0, a.jsx)("td", {
                          className: "px-1 py-1.5 w-40 actions-cell",
                          "data-no-click": "true",
                          onClick: e => e.stopPropagation(),
                          children: (0, a.jsxs)("div", {
                            className: "flex space-x-0.5",
                            children: [(0, a.jsx)("button", {
                              onClick: () => T(e),
                              className: "flex items-center px-1.5 py-0.5 bg-blue-100 text-blue-800 rounded hover:bg-blue-200 text-xs",
                              title: "View object details",
                              children: (0, a.jsx)("span", {
                                children: "Info"
                              })
                            }), (0, a.jsx)("button", {
                              onClick: () => eF(e),
                              className: "flex items-center px-1.5 py-0.5 bg-purple-100 text-purple-800 rounded hover:bg-purple-200 text-xs",
                              title: "Copy local file path",
                              children: (0, a.jsx)("span", {
                                children: "Path"
                              })
                            }), (0, a.jsx)("button", {
                              onClick: () => er({
                                isOpen: !0,
                                object: e,
                                loading: !1
                              }),
                              className: "flex items-center px-1 py-0.5 bg-red-100 text-red-800 rounded hover:bg-red-200 text-xs",
                              title: "Delete object",
                              children: (0, a.jsx)(u, {
                                className: "h-2 w-2"
                              })
                            })]
                          })
                        })]
                      }, e.uid))
                    })]
                  })
                })
              }), es > 1 && (0, a.jsxs)("div", {
                className: "flex items-center justify-between px-2 py-2 border-t bg-muted/20 flex-shrink-0",
                children: [(0, a.jsxs)("div", {
                  className: "text-xs text-muted-foreground",
                  children: [O, " objects • Page ", Q, " of ", es]
                }), (0, a.jsx)("div", {
                  className: "flex-1 flex justify-center",
                  children: ey && (0, a.jsx)("div", {
                    className: "text-xs text-muted-foreground italic",
                    children: ey
                  })
                }), (0, a.jsxs)("div", {
                  className: "flex items-center space-x-1",
                  children: [(0, a.jsxs)("button", {
                    onClick: () => eE(Q - 1),
                    disabled: Q <= 1,
                    className: "flex items-center space-x-1 px-2 py-1 border rounded hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed text-xs",
                    children: [(0, a.jsx)(p.Z, {
                      className: "h-3 w-3"
                    }), (0, a.jsx)("span", {
                      children: "Prev"
                    })]
                  }), (0, a.jsx)("div", {
                    className: "flex items-center space-x-1",
                    children: Array.from({
                      length: Math.min(3, es)
                    }, (e, t) => {
                      let s;
                      return s = es <= 3 ? t + 1 : Q <= 2 ? t + 1 : Q >= es - 1 ? es - 2 + t : Q - 1 + t, (0, a.jsx)("button", {
                        onClick: () => eE(s),
                        className: "px-2 py-1 text-xs rounded ".concat(Q === s ? "bg-blue-100 text-blue-800" : "hover:bg-muted"),
                        children: s
                      }, s)
                    })
                  }), (0, a.jsxs)("button", {
                    onClick: () => eE(Q + 1),
                    disabled: Q >= es,
                    className: "flex items-center space-x-1 px-2 py-1 border rounded hover:bg-muted disabled:opacity-50 disabled:cursor-not-allowed text-xs",
                    children: [(0, a.jsx)("span", {
                      children: "Next"
                    }), (0, a.jsx)(h.Z, {
                      className: "h-3 w-3"
                    })]
                  })]
                })]
              }), es <= 1 && (0, a.jsx)("div", {
                className: "flex items-center justify-center px-2 py-2 border-t bg-muted/20 flex-shrink-0",
                children: ey && (0, a.jsx)("div", {
                  className: "text-xs text-muted-foreground italic",
                  children: ey
                })
              })]
            })
          }), Z && (0, a.jsx)("div", {
            className: "fixed inset-0 bg-black/50 flex items-center justify-center p-2 z-50",
            onClick: () => {
              T(null), ec(!1), ex(null)
            },
            children: (0, a.jsxs)("div", {
              className: "bg-background rounded-lg max-w-4xl max-h-[95vh] overflow-y-auto w-full",
              onClick: e => e.stopPropagation(),
              children: [(0, a.jsx)("div", {
                className: "sticky top-0 bg-background border-b px-4 py-2",
                children: (0, a.jsxs)("div", {
                  className: "flex items-center justify-between",
                  children: [(0, a.jsx)("h2", {
                    className: "text-lg font-semibold",
                    children: Z.name
                  }), (0, a.jsx)("button", {
                    onClick: () => {
                      T(null), ec(!1), ex(null)
                    },
                    className: "text-muted-foreground hover:text-foreground",
                    children: "✕"
                  })]
                })
              }), (0, a.jsxs)("div", {
                className: "p-4 space-y-4",
                children: [(0, a.jsxs)("div", {
                  className: "grid grid-cols-2 gap-4",
                  children: [(0, a.jsxs)("div", {
                    children: [(0, a.jsx)("h3", {
                      className: "font-semibold text-sm mb-2",
                      children: "Object Details"
                    }), (0, a.jsxs)("div", {
                      className: "space-y-2 text-sm",
                      children: [(0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "UID:"
                        }), " ", (0, a.jsx)("span", {
                          className: "font-mono text-xs",
                          children: Z.uid
                        })]
                      }), (0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "Owner:"
                        }), " ", Z.email]
                      }), (0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "Created:"
                        }), " ", eB(Z.created_at)]
                      }), (0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "Updated:"
                        }), " ", eB(Z.updated_at)]
                      })]
                    })]
                  }), (0, a.jsxs)("div", {
                    children: [(0, a.jsx)("h3", {
                      className: "font-semibold text-sm mb-2",
                      children: "Files"
                    }), (0, a.jsxs)("div", {
                      className: "space-y-2 text-sm",
                      children: [(0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "Private:"
                        }), " ", Z.file_exists.private ? "✓ Available" : "✗ Not found"]
                      }), (0, a.jsxs)("div", {
                        children: [(0, a.jsx)("span", {
                          className: "font-medium",
                          children: "Mock:"
                        }), " ", Z.file_exists.mock ? "✓ Available" : "✗ Not found"]
                      })]
                    })]
                  })]
                }), (0, a.jsxs)("div", {
                  children: [(0, a.jsxs)("div", {
                    className: "flex items-center justify-between mb-2",
                    children: [(0, a.jsx)("h3", {
                      className: "font-semibold text-sm",
                      children: "Permissions"
                    }), (e => {
                      var t;
                      let s = (null == k ? void 0 : null === (t = k.syftbox) || void 0 === t ? void 0 : t.user_email) || "";
                      return e.email === s || e.permissions.syftobject.includes(s)
                    })(Z) && !eo && (0, a.jsx)("button", {
                      onClick: () => {
                        Z && (ex(JSON.parse(JSON.stringify(Z.permissions))), ec(!0))
                      },
                      className: "px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200",
                      children: "Edit"
                    }), eo && (0, a.jsxs)("div", {
                      className: "flex space-x-1",
                      children: [(0, a.jsxs)("button", {
                        onClick: eM,
                        disabled: em,
                        className: "px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200 disabled:opacity-50 flex items-center space-x-1",
                        children: [em && (0, a.jsx)(f.Z, {
                          className: "h-3 w-3 animate-spin"
                        }), (0, a.jsx)("span", {
                          children: em ? "Saving..." : "Save"
                        })]
                      }), (0, a.jsx)("button", {
                        onClick: () => {
                          ec(!1), ex(null)
                        },
                        className: "px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded hover:bg-gray-200",
                        children: "Cancel"
                      })]
                    })]
                  }), eo && ed ? (0, a.jsx)(b, {
                    permissions: ed,
                    onAddPermission: (e, t) => {
                      if (!ed || !t.trim()) return;
                      let s = {
                        ...ed
                      };
                      s[e].includes(t.trim()) || (s[e] = [...s[e], t.trim()]), ex(s)
                    },
                    onRemovePermission: (e, t) => {
                      if (!ed) return;
                      let s = {
                        ...ed
                      };
                      s[e] = s[e].filter(e => e !== t), ex(s)
                    }
                  }) : (0, a.jsxs)("div", {
                    className: "grid grid-cols-3 gap-4 text-xs",
                    children: [(0, a.jsxs)("div", {
                      children: [(0, a.jsx)("h4", {
                        className: "font-medium text-green-700 mb-1",
                        children: "Private Data"
                      }), (0, a.jsxs)("div", {
                        className: "space-y-1",
                        children: [(0, a.jsxs)("div", {
                          children: [(0, a.jsx)("span", {
                            className: "font-medium",
                            children: "Read:"
                          }), " ", Z.permissions.private_read.length > 0 ? Z.permissions.private_read.join(", ") : "None"]
                        }), (0, a.jsxs)("div", {
                          children: [(0, a.jsx)("span", {
                            className: "font-medium",
                            children: "Write:"
                          }), " ", Z.permissions.private_write.length > 0 ? Z.permissions.private_write.join(", ") : "None"]
                        })]
                      })]
                    }), (0, a.jsxs)("div", {
                      children: [(0, a.jsx)("h4", {
                        className: "font-medium text-blue-700 mb-1",
                        children: "Mock Data"
                      }), (0, a.jsxs)("div", {
                        className: "space-y-1",
                        children: [(0, a.jsxs)("div", {
                          children: [(0, a.jsx)("span", {
                            className: "font-medium",
                            children: "Read:"
                          }), " ", Z.permissions.mock_read.length > 0 ? Z.permissions.mock_read.join(", ") : "None"]
                        }), (0, a.jsxs)("div", {
                          children: [(0, a.jsx)("span", {
                            className: "font-medium",
                            children: "Write:"
                          }), " ", Z.permissions.mock_write.length > 0 ? Z.permissions.mock_write.join(", ") : "None"]
                        })]
                      })]
                    }), (0, a.jsxs)("div", {
                      children: [(0, a.jsx)("h4", {
                        className: "font-medium text-purple-700 mb-1",
                        children: "Syft Object"
                      }), (0, a.jsx)("div", {
                        className: "space-y-1",
                        children: (0, a.jsxs)("div", {
                          children: [(0, a.jsx)("span", {
                            className: "font-medium",
                            children: "Access:"
                          }), " ", Z.permissions.syftobject.length > 0 ? Z.permissions.syftobject.join(", ") : "None"]
                        })
                      })]
                    })]
                  })]
                }), Z.description && (0, a.jsxs)("div", {
                  children: [(0, a.jsx)("h3", {
                    className: "font-semibold text-sm mb-2",
                    children: "Description"
                  }), (0, a.jsx)("p", {
                    className: "text-sm text-muted-foreground",
                    children: Z.description
                  })]
                }), (0, a.jsxs)("div", {
                  children: [(0, a.jsx)("h3", {
                    className: "font-semibold text-sm mb-2",
                    children: "URLs"
                  }), (0, a.jsxs)("div", {
                    className: "space-y-2 text-xs font-mono",
                    children: [(0, a.jsxs)("div", {
                      children: [(0, a.jsx)("span", {
                        className: "font-medium",
                        children: "Private:"
                      }), " ", Z.private_url]
                    }), (0, a.jsxs)("div", {
                      children: [(0, a.jsx)("span", {
                        className: "font-medium",
                        children: "Mock:"
                      }), " ", Z.mock_url]
                    }), (0, a.jsxs)("div", {
                      children: [(0, a.jsx)("span", {
                        className: "font-medium",
                        children: "Syft Object:"
                      }), " ", Z.syftobject_url]
                    })]
                  })]
                }), Z.metadata && Object.keys(Z.metadata).length > 0 && (0, a.jsxs)("div", {
                  children: [(0, a.jsx)("h3", {
                    className: "font-semibold text-sm mb-2",
                    children: "Metadata"
                  }), (0, a.jsx)("pre", {
                    className: "text-xs bg-muted/20 p-3 rounded overflow-auto max-h-40",
                    children: JSON.stringify(Z.metadata, null, 2)
                  })]
                })]
              })]
            })
          }), el.isOpen && (0, a.jsx)("div", {
            className: "fixed inset-0 bg-black/50 flex items-center justify-center z-50",
            style: { padding: "5vh 5vw" },
            onClick: () => en({
              isOpen: !1,
              title: "",
              content: "",
              editedContent: "",
              loading: !1,
              saving: !1,
              fileType: null,
              objectUid: null,
              canWrite: !1
            }),
                          children: (0, a.jsxs)("div", {
              className: "bg-background rounded-lg overflow-hidden w-full h-full flex flex-col",
              onClick: e => e.stopPropagation(),
              children: [(0, a.jsx)("div", {
                className: "bg-background border-b px-3 py-1 flex-shrink-0",
                children: (0, a.jsxs)("div", {
                  className: "flex items-center justify-between",
                  children: [(0, a.jsx)("h2", {
                    className: "text-lg font-semibold",
                    children: el.title
                  }), (0, a.jsxs)("div", {
                    className: "flex items-center space-x-2",
                    children: [(0, a.jsx)("button", {
                      onClick: async () => {
                        let obj = I.find(obj => obj.uid === el.objectUid);
                        if (obj) {
                          let path = "";
                          try {
                            // Try to get the actual file path from the API
                            let response = await fetch("".concat("", "/api/objects/").concat(obj.uid));
                            if (response.ok) {
                              let data = await response.json();
                              if (el.fileType === "mock" && data.file_paths && data.file_paths.mock) {
                                path = data.file_paths.mock;
                              } else if (el.fileType === "private" && data.file_paths && data.file_paths.private) {
                                path = data.file_paths.private;
                              }
                            }
                            
                            // Fallback to constructing from URL if API doesn't have file_paths
                            if (!path) {
                              let url = el.fileType === "mock" ? obj.mock_url : obj.private_url;
                              if (url) {
                                let cleanUrl = url.replace("syft://", "");
                                let email = cleanUrl.split("/")[0];
                                let filePath = "/" + cleanUrl.split("/").slice(1).join("/");
                                path = "~/SyftBox/datasites/".concat(email).concat(filePath);
                              }
                            }
                            
                            if (path) await eA(path);
                            else throw Error("Could not determine local path");
                          } catch (error) {
                            let fallbackUrl = el.fileType === "mock" ? obj.mock_url : obj.private_url;
                            await eA(fallbackUrl || "Path not available");
                          }
                        }
                      },
                      className: "px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200",
                      children: "Copy Local Path"
                    }), (0, a.jsx)("button", {
                      onClick: () => {
                        if (el.content) eA(el.content);
                      },
                      className: "px-2 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200",
                      children: "Copy File"
                  }), (0, a.jsx)("button", {
                    onClick: () => en({
                      isOpen: !1,
                      title: "",
                      content: "",
                      editedContent: "",
                      loading: !1,
                      saving: !1,
                      fileType: null,
                      objectUid: null,
                      canWrite: !1
                    }),
                    className: "text-muted-foreground hover:text-foreground",
                    children: "✕"
                    })]
                  })]
                })
              }), (0, a.jsx)("div", {
                className: "flex-1 overflow-hidden p-2 flex flex-col min-h-0",
                children: el.loading ? (0, a.jsxs)("div", {
                  className: "flex items-center justify-center h-32",
                  children: [(0, a.jsx)(f.Z, {
                    className: "h-6 w-6 animate-spin text-blue-600"
                  }), (0, a.jsx)("span", {
                    className: "ml-2",
                    children: "Loading file content..."
                  })]
                }) : (0, a.jsxs)(a.Fragment, {
                  children: [(0, a.jsx)("textarea", {
                    value: el.editedContent,
                    onChange: e => en(t => ({
                      ...t,
                      editedContent: e.target.value
                    })),
                    className: "flex-1 w-full text-sm font-mono bg-muted/20 p-2 rounded border resize-none focus:ring-2 focus:ring-primary focus:border-transparent min-h-[60vh]",
                    placeholder: "File content...",
                    readOnly: !el.canWrite
                                      }), (0, a.jsxs)("div", {
                      className: "flex items-center justify-between mt-2",
                    children: [(0, a.jsx)("div", {
                      className: "text-xs text-muted-foreground",
                      children: el.canWrite ? "You can edit and save this file" : "You don't have write permission for this file"
                    }), (0, a.jsxs)("div", {
                      className: "flex space-x-2",
                      children: [(0, a.jsx)("button", {
                        onClick: () => en(e => ({
                          ...e,
                          editedContent: e.content
                        })),
                        disabled: el.editedContent === el.content,
                        className: "px-3 py-1 text-sm bg-secondary text-secondary-foreground rounded hover:bg-secondary/90 disabled:opacity-50",
                        children: "Reset"
                      }), (0, a.jsxs)("button", {
                        onClick: eL,
                        disabled: !el.canWrite || el.saving || el.editedContent === el.content,
                        className: "px-3 py-1 text-sm bg-green-100 text-green-800 rounded hover:bg-green-200 disabled:opacity-50 flex items-center space-x-1",
                        children: [el.saving && (0, a.jsx)(f.Z, {
                          className: "h-3 w-3 animate-spin"
                        }), (0, a.jsx)("span", {
                          children: el.saving ? "Saving..." : "Save"
                        })]
                      })]
                    })]
                  })]
                })
              })]
            })
          }), ei.isOpen && (0, a.jsx)("div", {
            className: "fixed inset-0 bg-black/50 flex items-center justify-center p-2 z-50",
            onClick: () => er({
              isOpen: !1,
              object: null,
              loading: !1
            }),
            children: (0, a.jsxs)("div", {
              className: "bg-background rounded-lg max-w-md w-full p-6",
              onClick: e => e.stopPropagation(),
              children: [(0, a.jsxs)("div", {
                className: "flex items-center space-x-3 mb-4",
                children: [(0, a.jsx)("div", {
                  className: "flex-shrink-0 w-10 h-10 mx-auto bg-red-100 rounded-full flex items-center justify-center",
                  children: (0, a.jsx)(u, {
                    className: "h-5 w-5 text-red-600"
                  })
                }), (0, a.jsxs)("div", {
                  children: [(0, a.jsx)("h3", {
                    className: "text-lg font-semibold text-gray-900",
                    children: ei.object ? "Delete Object" : "Delete Selected Objects"
                  }), (0, a.jsx)("p", {
                    className: "text-sm text-gray-500",
                    children: "This action cannot be undone."
                  })]
                })]
              }), (0, a.jsx)("div", {
                className: "mb-6",
                children: ei.object ? (0, a.jsxs)(a.Fragment, {
                  children: [(0, a.jsxs)("p", {
                    className: "text-sm text-gray-700",
                    children: ['Are you sure you want to delete "', (0, a.jsx)("span", {
                      className: "font-medium",
                      children: ei.object.name
                    }), '"?']
                  }), (0, a.jsx)("p", {
                    className: "text-xs text-gray-500 mt-2",
                    children: "This will permanently delete all associated files (private, mock, and syft object files)."
                  })]
                }) : (0, a.jsxs)(a.Fragment, {
                  children: [(0, a.jsxs)("p", {
                    className: "text-sm text-gray-700",
                    children: ["Are you sure you want to delete ", (0, a.jsxs)("span", {
                      className: "font-medium",
                      children: [V.size, " selected objects"]
                    }), "?"]
                  }), (0, a.jsx)("p", {
                    className: "text-xs text-gray-500 mt-2",
                    children: "This will permanently delete all associated files (private, mock, and syft object files) for all selected objects."
                  }), (0, a.jsxs)("div", {
                    className: "mt-3 max-h-20 overflow-y-auto",
                    children: [(0, a.jsx)("p", {
                      className: "text-xs text-gray-600 font-medium",
                      children: "Objects to delete:"
                    }), (0, a.jsx)("ul", {
                      className: "text-xs text-gray-500 mt-1",
                      children: I.filter(e => V.has(e.uid)).map(e => (0, a.jsxs)("li", {
                        children: ["• ", e.name]
                      }, e.uid))
                    })]
                  })]
                })
              }), (0, a.jsxs)("div", {
                className: "flex space-x-3 justify-end",
                children: [(0, a.jsx)("button", {
                  onClick: () => er({
                    isOpen: !1,
                    object: null,
                    loading: !1
                  }),
                  disabled: ei.loading,
                  className: "px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50",
                  children: "Cancel"
                }), (0, a.jsxs)("button", {
                  onClick: () => ei.object ? eR(ei.object.uid) : eI(),
                  disabled: ei.loading,
                  className: "px-4 py-2 text-sm font-medium text-red-800 bg-red-100 rounded-md hover:bg-red-200 disabled:opacity-50 flex items-center space-x-2",
                  children: [ei.loading && (0, a.jsx)(f.Z, {
                    className: "h-4 w-4 animate-spin"
                  }), (0, a.jsx)("span", {
                    children: ei.loading ? "Deleting..." : "Delete"
                  })]
                })]
              })]
            })
          })]
        })
      }
    },
    622: function(e, t, s) {
      var a = s(2265),
        l = Symbol.for("react.element"),
        n = Symbol.for("react.fragment"),
        i = Object.prototype.hasOwnProperty,
        r = a.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
        o = {
          key: !0,
          ref: !0,
          __self: !0,
          __source: !0
        };

      function c(e, t, s) {
        var a, n = {},
          c = null,
          d = null;
        for (a in void 0 !== s && (c = "" + s), void 0 !== t.key && (c = "" + t.key), void 0 !== t.ref && (d = t.ref), t) i.call(t, a) && !o.hasOwnProperty(a) && (n[a] = t[a]);
        if (e && e.defaultProps)
          for (a in t = e.defaultProps) void 0 === n[a] && (n[a] = t[a]);
        return {
          $$typeof: l,
          type: e,
          key: c,
          ref: d,
          props: n,
          _owner: r.current
        }
      }
      t.Fragment = n, t.jsx = c, t.jsxs = c
    },
    7437: function(e, t, s) {
      e.exports = s(622)
    },
    7865: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return i
        }
      });
      var a = s(2265),
        l = {
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
      var i = (e, t) => {
        let s = (0, a.forwardRef)(({
          color: s = "currentColor",
          size: i = 24,
          strokeWidth: r = 2,
          absoluteStrokeWidth: o,
          children: c,
          ...d
        }, x) => (0, a.createElement)("svg", {
          ref: x,
          ...l,
          width: i,
          height: i,
          stroke: s,
          strokeWidth: o ? 24 * Number(r) / Number(i) : r,
          className: `lucide lucide-${n(e)}`,
          ...d
        }, [...t.map(([e, t]) => (0, a.createElement)(e, t)), ...(Array.isArray(c) ? c : [c]) || []]));
        return s.displayName = `${e}`, s
      }
    },
    9799: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("Calendar", [
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
    4457: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("ChevronDown", [
        ["path", {
          d: "m6 9 6 6 6-6",
          key: "qrunsl"
        }]
      ])
    },
    6546: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("ChevronLeft", [
        ["path", {
          d: "m15 18-6-6 6-6",
          key: "1wnfg3"
        }]
      ])
    },
    4213: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("ChevronRight", [
        ["path", {
          d: "m9 18 6-6-6-6",
          key: "mthhwq"
        }]
      ])
    },
    7661: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("ChevronUp", [
        ["path", {
          d: "m18 15-6-6-6 6",
          key: "153udz"
        }]
      ])
    },
    7951: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("Filter", [
        ["polygon", {
          points: "22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3",
          key: "1yg77f"
        }]
      ])
    },
    2374: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("Globe", [
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
    892: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("Lock", [
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
    9915: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("RefreshCw", [
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
    3835: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("Search", [
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
    9839: function(e, t, s) {
      s.d(t, {
        Z: function() {
          return a
        }
      });
      let a = (0, s(7865).Z)("User", [
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
  }
]);