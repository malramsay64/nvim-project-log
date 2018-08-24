"
" Default Values
"
if !exists("g:project_log#mappings")
    let g:project_log#mappings = 1
endif
if !exists("g:project_log#logbooks")
    let g:project_log#logbooks = [$HOME.'/notes']
endif

if !exists("g:project_log#log_level")
    let g:project_log#log_level = 'INFO'
endif

if g:project_log#mappings
    nnoremap <silent> <space>l :ProjectLogToday<CR>
    nnoremap <silent> <space>i :ProjectLogIndex<CR>
    nnoremap <silent> <space>gi :ProjectLogUpdateIndex<CR>

    augroup project_log#Navigation
        autocmd!
        autocmd BufRead,BufNewFile */????-??-??.md nnoremap <buffer> <down> :ProjectLogPrevious<CR>
        autocmd BufRead,BufNewFile */????-??-??.md nnoremap <buffer> <up> :ProjectLogNext<CR>
    augroup END
endif
